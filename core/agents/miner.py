
import asyncio
import json
import sys
import os
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
    try:
        if sys.stdout.encoding.lower() != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Import robust LLM wrapper
from core.lib.llm_utils import SafeLLM, try_parse_json
from core.lib.metrics_logger import logger
from core.lib.workflow_utils import extract_workflow_keywords, score_element_relevance
from core.lib.dom_driver import DOM_EXTRACTION_SCRIPT
from core.lib.image_optimizer import ImageOptimizer

load_dotenv()

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
2. **DETECT BLOCKERS**: Look for popups, newsletter signups, cookie banners, or "overlay backdrops".
   - If an element is a "Close" button for a popup (even if it's just an 'X' icon), mark it clearly.
   - If the main content is dimmed/blurred behind an overlay, note this in `mission_status`.
3. Provide a high-level `page_summary` describing the page's purpose and state.
4. For each element, identify its "Semantic Surroundings".
5. Provide a `playwright_hint` for important elements.
6. Suggest the MOST likely sequence of target elements by ID to achieve the goal.

**OUTPUT SCHEMA**:
{
  "page_summary": {
    "title": "...",
    "purpose": "...",
    "state": "logged_in | login_screen | error | dashboard | blocked_by_modal",
    "mission_status": "Briefly state if the goal is visible or if a popup is blocking the view."
  },
  "important_elements": [
    {
       "elementId": 1,
       "semantic_context": "e.g., 'Close button (X icon) for newsletter popup'",
       "confidence": "high | medium | low",
       "playwright_hint": "e.g., getByRole('button', name='Close')"
    }
  ],
  "blocking_elements": [
    {"elementId": 4, "description": "Newsletter modal backdrop"}
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
            if frame.is_detached(): continue
            frame_res = await frame.evaluate(DOM_EXTRACTION_SCRIPT, current_id)
            frame_elements = frame_res.get('elements', [])
            for el in frame_elements:
                el['frame_context'] = frame.name or frame.url
            all_elements.extend(frame_elements)
            current_id = frame_res.get('lastId', current_id)
        except Exception:
            pass

    return all_elements

def optimize_image(image_bytes: bytes, context: dict = None) -> str:
    """
    Advanced image optimization with context-aware strategies.
    """
    try:
        # Detected step type
        step_type = context.get('step_type', 'general') if context else 'general'
        prev_url = context.get('prev_url') if context else None
        current_url = context.get('current_url') if context else None
        
        # Strategy 5: Skip/Minimize if URL unchanged
        if prev_url and current_url and prev_url == current_url:
            print(colored(f"   ⚡ Smart Skip: URL unchanged, using minimal optimization", "magenta"))
            step_type = "search" # Most aggressive crop/resize
            
        # Use ImageOptimizer
        b64 = ImageOptimizer.context_aware_optimization(image_bytes, step_type)
        
        # Log reduction
        original_size = len(image_bytes)
        decoded = base64.b64decode(b64)
        new_size = len(decoded)
        reduction = (1 - (new_size / original_size)) * 100
        
        strategy_label = {
            'search': '🔍 Search-optimized',
            'button': '🎯 Button-optimized',
            'form': '📝 Form-optimized',
            'verification': '✓ Verify-optimized',
            'general': '📸 Optimized'
        }.get(step_type, '📸 Optimized')
        
        print(colored(f"   📉 {strategy_label}: {original_size//1024}KB -> {new_size//1024}KB ({reduction:.1f}% reduced)", "grey"))
        return b64
        
    except Exception as e:
        # Fallback to simple compression if ImageOptimizer fails
        try:
            from PIL import Image
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=30, optimize=True)
            return base64.b64encode(output.getvalue()).decode('utf-8')
        except:
            return base64.b64encode(image_bytes).decode('utf-8')

async def analyze_page(page: Page, url: str, user_goal=None):
    """
    Performs a Vision + DOM reconciliation.
    """
    print(colored(f"🔍 Mining Page (2026 Strategy): {url}", "cyan"))
    
    # --- HYDRATION GUARD ---
    # Detect if we are in a 'skeleton/blocked' state
    for i in range(5): # Up to 5 retries (15s total)
        is_skeleton = await page.evaluate("""
            () => {
                if (!document.body) return true; // Treat as skeleton if body is missing
                const links = document.querySelectorAll('a');
                const hasSkip = Array.from(links).some(a => a.innerText.toLowerCase().includes('skip to'));
                const hasBodyContent = document.body.innerText.length > 500;
                // If we see 'skip to products' but the page is very light, it's a skeleton
                return hasSkip && !hasBodyContent;
            }
        """)
        
        if is_skeleton:
            print(colored(f"   ⏳ [Retry {i+1}] Detected Skeleton/Blocked state. Waiting for hydration...", "yellow"))
            if i == 1: # On second retry, try a hard reload
                print(colored("   🔄 [Skeleton Guard] Hard Reloading page to bypass ghost block...", "magenta"))
                await page.reload(wait_until="networkidle", timeout=60000)
            await asyncio.sleep(3)
        else:
            break

    # Final check for meaningful elements
    try:
        await page.wait_for_selector('button, .price, .product-details, h1', timeout=10000)
    except:
        print(colored("   ⏳ Meaningful elements slow. Waiting 3s for settlement...", "yellow"))
        await asyncio.sleep(3)


    # 1. Background Cleanup
    await page.evaluate("""
        () => {
            const noise = [
                'iframe[id*="google"]', 'iframe[src*="doubleclick"]',
                '.ad', '.ads', '.advertisement', '.social-share',
                '#cookies-banner', '[class*="cookie-banner"]',
                '.vignette', '#credential_picker_container'
            ];
            document.querySelectorAll(noise.join(',')).forEach(el => el.remove());
        }
    """)

    # 2. Parallel DOM + Vision Capture
    print(colored(f"🚀 Parallel Capture: DOM + Screenshot...", "grey"))
    elements_task = extract_all_elements(page)
    screenshot_task = page.screenshot(type="jpeg", quality=60)
    
    elements, screenshot_bytes = await asyncio.gather(elements_task, screenshot_task)
    
    # Determine step type for optimization
    step_type = "general"
    if user_goal:
        goal_lower = user_goal.lower()
        if "search" in goal_lower: step_type = "search"
        elif any(k in goal_lower for k in ["cart", "checkout", "button", "click", "buy"]): step_type = "button"
        elif any(k in goal_lower for k in ["form", "fill", "type", "login"]): step_type = "form"
        elif any(k in goal_lower for k in ["verify", "check", "confirm"]): step_type = "verification"

    b64_img = optimize_image(screenshot_bytes, context={
        'step_type': step_type,
        'prev_url': getattr(analyze_page, '_last_url', None),
        'current_url': url
    })
    analyze_page._last_url = url
    
    # --- FOCUSED MINING FILTER ---
    keywords = extract_workflow_keywords(user_goal)
    scored_elements = []
    
    if keywords:
        print(colored(f"   🎯 Focused Mining: Filtering with {len(keywords)} workflow keywords...", "cyan"))
        for el in elements:
            score = score_element_relevance(el, keywords)
            if score >= 0.7:
                scored_elements.append(el)
        
        reduction = (1 - (len(scored_elements) / len(elements))) * 100 if len(elements) > 0 else 0
        print(colored(f"   📉 Focus Filter: Reduced {len(elements)} -> {len(scored_elements)} candidates ({reduction:.1f}% reduction)", "cyan"))
        elements = scored_elements

    # --- VISION FILTERING (No-LLM) ---
    from core.lib.vision_miner import VisionMiner
    import concurrent.futures

    visible_elements = []
    if len(elements) > 0:
        print(colored(f"   👁️ Vision Filter: Checking {len(elements)} elements in parallel...", "grey"))
        total_focused = len(elements)
        
        def verify_el(el):
            w, h = el['rect']['width'], el['rect']['height']
            if 0 < w < 800 and 0 < h < 600:
                res = VisionMiner.verify_visibility(
                    screenshot_bytes, 
                    el['rect']['x'], el['rect']['y'], w, h
                )
                if res['is_visible']:
                    el['is_visible'] = True
                    el['contrast_score'] = res.get('contrast_score', 0)
                    return el
            return None 

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(verify_el, elements))
        
        visible_elements = [r for r in results if r is not None]
        verified_count = len(visible_elements)
                
        if verified_count == 0 and total_focused > 0:
            print(colored("   ⚠️ Vision Filter was too strict (0 results). Falling back to focused DOM elements.", "yellow"))
            # Keep the elements as they were before vision filter
        else:
            reduction = (1 - (verified_count / total_focused)) * 100 if total_focused > 0 else 0
            print(colored(f"   📉 Vision Filter: Reduced {total_focused} -> {verified_count} elements ({reduction:.1f}% reduction)", "cyan"))
            elements = visible_elements

    
    # --- VISION-FIRST OPTIMIZATION ---
    if len(elements) > 0 and len(elements) < 10: 
         print(colored(f"⚡ Vision-First Optimization: Small target set ({len(elements)}). Passing directly to Planner.", "green", attrs=["bold"]))
         browser_title = await page.title()
         return {
            "summary": {"title": browser_title, "purpose": "Vision-Verified Page", "state": "active"},
            "elements": elements,
            "url": url,
            "verification": f"VisionMiner Verified {len(elements)} elements"
        }

    # 3. LLM Reconciliation
    messages = [
        ("system", SYSTEM_PROMPT_ANALYST),
        ("human", [
            {"type": "text", "text": f"User Goal: {user_goal or 'Explore page'}\nInteractive Elements: {json.dumps(elements[:100], indent=2)}"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
        ])
    ]
    
    try:
        print(colored(f"   🤖 Requesting Vision Analysis for {len(elements)} elements...", "grey"))
        resp = await llm.ainvoke(messages)
        mindmap = try_parse_json(resp.content)
        
        enriched_elements = []
        element_map = {str(e['elementId']): e for e in elements}
        
        for imp in mindmap.get('important_elements', []):
            eid = str(imp.get('elementId'))
            if eid in element_map:
                el = element_map[eid]
                el['semantic_context'] = imp.get('semantic_context')
                el['playwright_hint'] = imp.get('playwright_hint')
                el['confidence'] = imp.get('confidence')
                enriched_elements.append(el)
        
        return {
            "summary": mindmap.get('page_summary', {}),
            "elements": enriched_elements or elements, 
            "url": url,
            "visibility_notes": mindmap.get('visibility_notes', '')
        }
    except Exception as e:
        print(colored(f"   ⚠️ Vision analysis failed: {e}. Falling back to focused DOM.", "yellow"))
        return {
            "summary": {"purpose": "Fallback Page", "state": "error"},
            "elements": elements,
            "url": url
        }

if __name__ == "__main__":
    async def test():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://www.google.com")
            res = await analyze_page(page, "https://www.google.com")
            print(json.dumps(res, indent=2))
            await browser.close()
    
    asyncio.run(test())
