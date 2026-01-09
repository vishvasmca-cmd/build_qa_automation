
import asyncio
import json
import sys

# Windows Unicode Fix
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

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
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Import robust LLM wrapper
# Import robust LLM wrapper
from core.lib.llm_utils import SafeLLM

# Import Metrics Logger
# Import Metrics Logger
from core.lib.metrics_logger import logger

# Import the 2026-style driver
# Import the 2026-style driver
from core.lib.dom_driver import DOM_EXTRACTION_SCRIPT

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
    # Check Cache First (File-Based Persistence)
    cache_path = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "vision_cache.json")
    
    # Load Cache
    if not hasattr(analyze_page, "cache"):
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    analyze_page.cache = json.load(f)
            except: 
                analyze_page.cache = {}
        else:
            analyze_page.cache = {}

    # Robust Cache Key: URL + Title + Round(ElementCount, -1) to handle minor DOM fluctations
    # e.g. 104 elements -> 100, 106 -> 110. This prevents cache bust on dynamic ads.
    ele_count_approx = round(len(elements) / 10) * 10
    page_title = elements[0].get('text', '') if elements else "NoTitle" # Very rough proxy if title tag missing
    
    # Try to find title in elements
    for e in elements[:10]:
        if e['tagName'] == 'TITLE': 
            page_title = e['text']
            break
            
    cache_key = hashlib.md5(f"{url}|{user_goal}|{page_title}|{ele_count_approx}".encode()).hexdigest()
    current_time = __import__('time').time()
    
    cached = analyze_page.cache.get(cache_key)
    # 24 Hour TTL for stability testing
    if cached and (current_time - cached['timestamp'] < 86400):
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
        
        resp = await llm.ainvoke([message])
        analysis = try_parse_json(resp.content) or {}
        
        # Save to cache & Persist to Disk
        analyze_page.cache[cache_key] = {
            'analysis': analysis,
            'timestamp': current_time
        }
        try:
             # Atomic write prevention (simple)
             os.makedirs(os.path.dirname(cache_path), exist_ok=True)
             with open(cache_path, "w") as f:
                 json.dump(analyze_page.cache, f)
        except Exception as e:
            print(colored(f"⚠️ Cache Write Error: {e}", "yellow"))
        
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


class BatchMiner:
    """
    Phase 2: Automation Discovery Engine.
    Processes artifacts from Phase 1 to build a robust Page Object Model blueprint.
    """
    def __init__(self, project_path):
        self.project_path = project_path
        self.output_dir = os.path.join(project_path, "outputs")
        self.snapshot_dir = os.path.join(project_path, "snapshots")
        self.trace_path = os.path.join(self.output_dir, "trace.json")
        self.elements_path = os.path.join(self.output_dir, "discovered_elements.json")
        self.page_models = {}

    async def mine(self):
        print(colored("⛏️ Starting Batch Mining...", "cyan"))
        
        # 1. Load Artifacts
        if not os.path.exists(self.trace_path):
            print(colored(f"❌ No trace.json found at {self.trace_path}. Skipping Mining.", "red"))
            return
            
        with open(self.trace_path, "r") as f:
            trace_data = json.load(f)
            
        trace = trace_data.get("trace", [])
        
        # 2. Group by Page
        pages = {}
        for step in trace:
            page_name = step.get("page_name", "UnknownPage")
            if page_name not in pages:
                pages[page_name] = {
                    "url": step.get("url"),
                    "screenshots": [],
                    "actions": []
                }
            if step.get("screenshot"):
                pages[page_name]["screenshots"].append(step.get("screenshot"))
            pages[page_name]["actions"].append(step)

        # 3. Analyze Each Page
        print(colored(f"🔍 Discovered {len(pages)} unique pages.", "blue"))
        
        for page_name, data in pages.items():
            await self._analyze_page_model(page_name, data)

        # 4. Save Page Models
        output_path = os.path.join(self.output_dir, "page_models.json")
        with open(output_path, "w") as f:
            json.dump(self.page_models, f, indent=2)
            
        print(colored(f"✅ Page Models saved to {output_path}", "green"))

    async def _analyze_page_model(self, page_name, data):
        print(colored(f"   👉 Analyzing {page_name}...", "yellow"))
        
        # Select best screenshot (last one is usually most stable)
        if not data["screenshots"]:
            print(colored(f"      ⚠️ No screenshots for {page_name}", "red"))
            return
            
        screenshot_name = data["screenshots"][-1]
        screenshot_path = os.path.join(self.snapshot_dir, screenshot_name)
        
        if not os.path.exists(screenshot_path):
             # Try legacy path fallback
             screenshot_path = os.path.join(self.output_dir, screenshot_name)
        
        if not os.path.exists(screenshot_path):
            print(colored(f"      ⚠️ Screenshot not found: {screenshot_path}", "red"))
            return

        # Prepare for LLM
        with open(screenshot_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode('utf-8')

        # Prompt for Page Modeling
        prompt = f"""
        You are an Automation Architect. Analyze the screenshot of '{page_name}'.
        URL: {data['url']}
        
        **TASK**:
        1. Identify the **Primary Purpose** of this page.
        2. Define **Robust Locators** for key interactive elements visible in the screenshot.
           - For each element, provide a PRIMARY locator (Role/TestID) and a BACKUP locator (CSS/Text).
           - The 'locator_strategy' field will be used to generate `primary.or_(backup)`.
        3. Identify **Critical Assertions** to verify this page is loaded (e.g., Title, Header text).
        
        **OUTPUT JSON SCHEMA**:
        {{
            "description": "Login page for customer access",
            "url_pattern": "/login",
            "elements": [
                {{
                    "name": "login_btn",
                    "type": "button",
                    "primary_locator": "get_by_role('button', name='Login')",
                    "backup_locator": "locator('#login-button')",
                    "description": "Main submission button"
                }}
            ],
            "assertions": [
                "expect(page).to_have_title('Login - Automation Exercise')",
                "expect(page.get_by_role('heading', name='Login')).to_be_visible()"
            ]
        }}
        """
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
            ]
        )
        
        try:
            resp = llm.invoke([message])
            model = try_parse_json(resp.content)
            if model:
                self.page_models[page_name] = model
        except Exception as e:
            print(colored(f"      ❌ Modeling failed: {e}", "red"))
