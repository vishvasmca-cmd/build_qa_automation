
import asyncio
import json
import os
import sys
import io
import base64
import hashlib
import time
from playwright.async_api import async_playwright, Page, Frame
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from termcolor import colored

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    pass # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import robust LLM wrapper
try:
    from .llm_utils import SafeLLM
except (ImportError, ValueError):
    from llm_utils import SafeLLM

# Import Metrics Logger
try:
    from .metrics_logger import logger
except ImportError:
    from metrics_logger import logger

# Import the 2026-style driver
try:
    from core.dom_driver import DOM_EXTRACTION_SCRIPT
except ImportError:
    from dom_driver import DOM_EXTRACTION_SCRIPT

load_dotenv()

# Initialize 2026-ready LLM (Vision-Capable)
# Initialize 2026-ready LLM (Vision-Capable)
llm = SafeLLM(
    model="gemini-2.0-flash",
    temperature=0.0,
    model_kwargs={"response_mime_type": "application/json"}
)

SYSTEM_PROMPT_ANALYST = """
You are a Vision-First Web Automation Analyst. 
Your goal is to reconcile a provided list of "Interactive Elements" with a screenshot of the page.

**TASK**:
1. Analyze the screenshot and the `interactive_elements` JSON.
2. Verify the accuracy of the element list. If you see a button in the screenshot that is NOT in the list, note it in `visibility_notes`.
3. Provide a high-level `page_summary` describing the page's purpose and state.
4. For each element, identify its "Semantic Surroundings" (e.g., "Next to Login text", "Inside navigation bar").
5. Provide a `playwright_hint` for important elements following this hierarchy:
   - Rank 1: `getByRole`, `getByLabel`, `getByPlaceholder`, `getByText`.
   - Rank 2: `getByTestId` (look for `data-test*` attributes).
   - Rank 3: CSS attributes (e.g., `button[type="submit"]`).
6. If the user goal is provided, suggest the MOST likely sequence of target elements by ID.

**OUTPUT SCHEMA**:
{
  "page_summary": {
    "title": "...",
    "purpose": "...",
    "state": "logged_in | login_screen | error | dashboard",
    "spatial_verification": "How many buttons/links did you see vs how many were in the list?"
  },
  "important_elements": [
    {
       "elementId": 1,
       "semantic_context": "Next to 'Forgot Password'",
       "confidence": "high | medium | low",
       "playwright_hint": "e.g., getByRole('button', name='Submit')"
    }
  ],
  "visibility_notes": "..."
}
"""

async def extract_all_elements(page: Page):
    """Extract elements from main page and all iframes with unique IDs."""
    all_elements = []
    current_id = 0
    
    # 1. Main Page
    try:
        main_res = await page.evaluate(DOM_EXTRACTION_SCRIPT, 0)
        all_elements.extend(main_res.get('elements', []))
        current_id = main_res.get('lastId', 0)
    except Exception as e:
        print(colored(f"   ⚠️ Error mining main frame: {e}", "yellow"))

    # 2. Frames
    for frame in page.frames:
        if frame == page.main_frame: continue
        try:
            # Check if frame is accessible
            if frame.is_detached(): continue
            frame_res = await frame.evaluate(DOM_EXTRACTION_SCRIPT, current_id)
            frame_elements = frame_res.get('elements', [])
            for el in frame_elements:
                el['frame_context'] = frame.name or frame.url
            all_elements.extend(frame_elements)
            current_id = frame_res.get('lastId', current_id)
        except Exception as e:
            # Often iframes are cross-origin and blocked from JS injection
            pass

    return all_elements

def try_parse_json(content):
    import re
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'\s*```', '', content)
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        if match:
            try: return json.loads(match.group(1))
            except: pass
    return None

async def analyze_page(page: Page, url: str, user_goal=None):
    """
    Performs a Vision + DOM reconciliation.
    Returns a unified Page Mindmap.
    """
    print(colored(f"🔍 Mining Page (2026 Strategy): {url}", "cyan"))
    
    # 1. Extract Structural Data
    elements = await extract_all_elements(page)
    
    # 2. Capture Visual State
    screenshot_bytes = await page.screenshot(type="jpeg", quality=85)
    b64_img = base64.b64encode(screenshot_bytes).decode('utf-8')
    
    # 3. LLM Reconciliation
    # Check Cache First
    cache_key = hashlib.md5(f"{url}|{user_goal}|{len(elements)}".encode()).hexdigest()
    current_time = __import__('time').time()
    
    # Simple in-memory cache: {hash: {'analysis': dict, 'timestamp': float}}
    if not hasattr(analyze_page, "cache"):
        analyze_page.cache = {}
        
    cached = analyze_page.cache.get(cache_key)
    if cached and (current_time - cached['timestamp'] < 300): # 5 Minute TTL
        print(colored("⚡ Cache Hit! Skipping Vision Analysis.", "green"))
        
        # Log Cache Hit
        logger.log_event(
            agent="Miner", 
            action="analyze_page_cache_hit", 
            duration=0.001, 
            metadata={"url": url}
        )
        
        analysis = cached['analysis']
    else:
        start_time = time.time()
        # Filter list to top 100 for token efficiency
        element_summary = [
            {"id": e['elementId'], "tag": e['tagName'], "text": e['text'], "type": e['type'], "center": e['center']} 
            for e in elements[:100]
        ]
    
        prompt = f"""
        URL: {url}
        Goal: {user_goal or "Understand the page structure"}
        Interactive Elements List (JSON): {json.dumps(element_summary)}
        
        Analyze the screenshot and verify the list. Answer 'how many buttons are on web page' in spatial_verification.
        """
    
        message = HumanMessage(
            content=[
                {"type": "text", "text": f"{SYSTEM_PROMPT_ANALYST}\n\n{prompt}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
            ]
        )
        
        resp = llm.invoke([message])
        analysis = try_parse_json(resp.content) or {}
        
        # Save to cache
        analyze_page.cache[cache_key] = {
            'analysis': analysis,
            'timestamp': current_time
        }
        
        # Log LLM Call
        duration = time.time() - start_time
        logger.log_event(
            agent="Miner", 
            action="analyze_page_llm_call", 
            duration=duration, 
            cost=0.005, # Est cost for flash vision
            metadata={"url": url, "elements": len(elements)}
        )


    try:
        # Merge analysis back to elements
        important_map = {str(item['elementId']): item for item in analysis.get('important_elements', [])}
        for el in elements:
            info = important_map.get(str(el['elementId']))
            if info:
                el['semantic_context'] = info.get('semantic_context')
                el['is_important'] = True
                el['playwright_hint'] = info.get('playwright_hint')

        return {
            "summary": analysis.get('page_summary', {}),
            "elements": elements,
            "url": url,
            "verification": analysis.get('page_summary', {}).get('spatial_verification', '')
        }

    except Exception as e:
        print(colored(f"❌ Miner LLM Error: {e}", "red"))
        return {
            "summary": {"purpose": "Fallback due to error"},
            "elements": elements,
            "url": url,
            "verification": "Error"
        }

if __name__ == "__main__":
    async def test():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://my.astound.com/login")
            await asyncio.sleep(2)
            result = await analyze_page(page, "https://my.astound.com/login", "Login to account")
            print(colored("\n--- Page Analysis Result ---", "green"))
            print(json.dumps(result['summary'], indent=2))
            print(f"Found {len(result['elements'])} elements.")
            print(f"Verification: {result['verification']}")
            await browser.close()
    asyncio.run(test())
