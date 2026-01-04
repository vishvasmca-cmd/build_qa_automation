import asyncio
import json
import os
from playwright.async_api import async_playwright, Page
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.0,
    model_kwargs={"response_mime_type": "application/json"}
)

SYSTEM_PROMPT_LOCATORS = """
You are a production-grade Web Scraping & Locator Mining Agent.
You MUST prioritize `data-test` attributes and Shadow DOM compatibility.

**MANDATORY OUTPUT FORMAT**:
{
  "visibleElements": [
    {
      "elementId": "el_0",
      "visibleText": "text",
      "role": "button",
      "center": {"x": 100, "y": 200},
      "locatorCandidates": [
         {
           "playwrightLocator": "page.locator(...)",
           "strength": "GOOD",
           "reason": "..."
         }
      ]
    }
  ]
}

**CRITICAL RULES:**
1. **NO HALLUCINATIONS**: If you see an input in the screenshot but it is NOT in the `visibleElements` list (or has no ID), **DO NOT** invent a locator on a nearby button.
2. **COORDINATE ACTIONS**: 
   - If a selector is complex or unstable, you MAY propose `page.mouse.click(x, y)` using the provided `center` coordinates. Mark strength as "FALLBACK".
   - **VISUAL FILL**: You can even use `page.mouse.click(x, y)` for "fill" actions. The agent will click the location and then simulate typing.
3. **FORM FIELDS vs BUTTONS**: 
   - NEVER suggest `fill()` on a "button" or "link" role. Only on "textbox", "input", "textarea".
   - If an input is missing from the DOM list, say "Input missing from DOM" in the summary.
4. **SHADOW DOM**: If the locator involves `shadowRoot`, use standard CSS/Playwright selectors as Playwright handles open shadow roots automatically (e.g., `page.locator('my-component >> input')`).

Output JSON only.
"""

SYSTEM_PROMPT_SUMMARY = """
You are a Website Analyst.
Given the text content and interactive elements:
1. `page_name`: Short name.
2. `domain_context`: E-commerce / Banking / SaaS / ISP.
3. `available_actions`: High-level user actions.
4. `form_fields_detected`: specific inputs visible.
5. `extracted_test_data`: Any credentials/data seen.

Output JSON only.
"""

async def extract_dom_snapshot(frame: Page):
    """
    Extracts visible interactables using recursive Shadow DOM traversal from a specific frame.
    """
    try:
        if frame.is_detached(): return {"interactables": [], "bodyText": ""}
        
        return await frame.evaluate("""() => {
            const interactables = [];
            const selector = 'button, a, input:not([type=hidden]), select, textarea, [role="button"], [role="textbox"], [role="searchbox"], [role="checkbox"], [role="radio"], [contenteditable], [data-test], [data-testid], .shopping_cart_link';
            
            function getVisibleText(el) {
                return (el.innerText || el.textContent || el.value || el.getAttribute('aria-label') || '').slice(0, 50).replace(/\\n/g, ' ').trim();
            }

            function isVisible(el) {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
            }

            function traverse(root) {
                if (!root) return;
                
                // 1. Check direct children matching selector
                const elements = root.querySelectorAll(selector);
                elements.forEach(el => {
                    if (!isVisible(el)) return;
                    
                    const rect = el.getBoundingClientRect();
                    interactables.push({
                        tag: el.tagName.toLowerCase(),
                        type: el.getAttribute('type') || '',
                        name: el.getAttribute('name') || '',
                        text: getVisibleText(el),
                        role: el.getAttribute('role') || el.tagName.toLowerCase(),
                        testId: el.getAttribute('data-testid') || el.getAttribute('data-test-id') || '',
                        customTestId: el.getAttribute('data-test') || '',
                        placeholder: el.getAttribute('placeholder') || '',
                        href: el.getAttribute('href') || '',
                        center: {
                            x: Math.round(rect.left + rect.width / 2),
                            y: Math.round(rect.top + rect.height / 2)
                        }
                    });
                });

                // 2. Walker for Shadow Roots
                const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, null, false);
                let node;
                while (node = walker.nextNode()) {
                    if (node.shadowRoot) {
                        traverse(node.shadowRoot);
                    }
                }
            }

            traverse(document);
            
            // Post-processing: Assign IDs based on visual order (Top-Left to Bottom-Right)
            interactables.sort((a, b) => (a.center.y * 10000 + a.center.x) - (b.center.y * 10000 + b.center.x));
            interactables.forEach((el, idx) => el.id = `el_${idx}`);

            const bodyText = document.body ? document.body.innerText.slice(0, 1000) : "";
            return { interactables, bodyText };
        }""")
    except Exception as e:
        return {"interactables": [], "bodyText": ""}

def try_parse_json(content):
    import re
    # Remove markdown blocks
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'\s*```', '', content)
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Look for the last { ... } block
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        if match:
            try: return json.loads(match.group(1))
            except: pass
    return None

async def analyze_page(page: Page, url: str, knowledge_context=None, cache_path="locator_cache.json", force_refresh=False):
    # 1. Extract DOM & Text (Multi-Frame)
    raw_elements = []
    body_text = ""
    
    # Main Frame
    main_data = await extract_dom_snapshot(page)
    raw_elements.extend(main_data['interactables'])
    body_text += main_data['bodyText']
    
    # Child Frames
    for frame in page.frames:
        if frame == page.main_frame: continue
        try:
            frame_data = await extract_dom_snapshot(frame)
            # Add frame context to elements
            for el in frame_data['interactables']:
                el['context'] = f"iframe[{frame.name or frame.url}]"
                # Coordinates in iframes are relative to the frame, which is tricky.
                # ideally we map them to main page coords, but for now we trust the selector execution context.
            raw_elements.extend(frame_data['interactables'])
        except: pass
    
    # Re-index global IDs
    for i, el in enumerate(raw_elements):
         el['id'] = f"el_{i}"

    # New: Deep Scan Fallback if no forms found on a likely login page
    if len([e for e in raw_elements if e['tag'] in ['input', 'textarea']]) == 0:
        print(colored("   🕵️‍♀️ Deep Scan: Standard mining found 0 inputs. Trying Playwright Native Scan...", "cyan"))
        try:
            native_inputs = await page.get_by_role("textbox").all()
            for i, inp in enumerate(native_inputs):
                try:
                    box = await inp.bounding_box()
                    if box:
                        # DEBUG: Print what we found
                        try:
                            ph = await inp.get_attribute("placeholder") or ""
                            nm = await inp.get_attribute("name") or ""
                            lbl = await inp.get_attribute("aria-label") or ""
                            print(colored(f"   🔎 Deep Scan Found: Input {i} | Name='{nm}' | PH='{ph}' | Label='{lbl}'", "cyan"))
                        except: pass

                        raw_elements.append({
                            "id": f"el_native_{i}",
                            "tag": "input",
                            "type": "text",
                            "role": "textbox",
                            "text": f"Native Input {i} ({nm or ph or lbl})",
                            "center": {"x": box['x'] + box['width']/2, "y": box['y'] + box['height']/2},
                            "locatorCandidates": [
                                {
                                    "playwrightLocator": f'page.get_by_role("textbox").nth({i})',
                                    "strength": "FALLBACK",
                                    "reason": "Deep Scan detected native input missing from DOM snapshot"
                                }
                            ]
                        })
                except: pass
        except: pass

    # Context string
    context_str = json.dumps(knowledge_context) if knowledge_context else "None"

    # 2. Check Cache
    cache_file = cache_path
    cache = {}
    if os.path.exists(cache_file) and not force_refresh:
        with open(cache_file, "r") as f:
            try: cache = json.load(f)
            except: pass
    
    # Hash based on coordinates too now to catch layout changes
    structure_sig = "".join([f"{el['tag']}{el['center']['x']}" for el in raw_elements])
    import hashlib
    content_hash = hashlib.md5(structure_sig.encode('utf-8')).hexdigest()
    cache_key = f"{url}_{content_hash}"
    
    if cache_key in cache:
        print(f"⚡ Using Cached Locators for: {url} (State Match)")
        return cache[cache_key]

    print(f"🕵️  Mining Page via Vision+DOM: {url}")
    
    # 3. Capture Visual context
    screenshot_bytes = await page.screenshot(type="jpeg", quality=80) 
    import base64
    b64_img = base64.b64encode(screenshot_bytes).decode('utf-8')
    
    # 4. Single multi-modal call
    element_slice = raw_elements[:200]
    
    COMBINED_PROMPT = f"""
    URL: {url}
    Context: {context_str}
    Visible Elements (with Coordinates): {json.dumps(element_slice)}
    
    {SYSTEM_PROMPT_SUMMARY}
    {SYSTEM_PROMPT_LOCATORS}
    
    **MANDATORY**: Return a valid JSON object.
    """
    
    from langchain_core.messages import HumanMessage
    msg = HumanMessage(
        content=[
            {"type": "text", "text": COMBINED_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
        ]
    )

    RESCUE_PROMPT = """
    CRITICAL ERROR: Previous JSON attempt failed. 
    Look at the image and the provided element list. 
    Just give me the TOP 5 most important interactive elements (buttons/links) you see.
    Format your response EXACTLY like this:
    {
      "summary": {"page_name": "Rescue Mode"},
      "locators": [
        {
          "elementId": "el_index",
          "visibleText": "text",
          "role": "button",
          "locatorCandidates": [{"playwrightLocator": "page.locator(...)", "strength": "GOOD"}]
        }
      ]
    }
    """

    try:
        # Attempt 1: Combined
        resp = llm.invoke([msg])
        payload = try_parse_json(resp.content)
        
        if not payload or "locators" not in payload:
            print(colored("   🚑 Combined Mining Failed. Triggering Advanced Rescue Strategy...", "yellow"))
            # Attempt 2: Rescue with focus on essentials
            rescue_msg = HumanMessage(
                content=[
                    {"type": "text", "text": f"{RESCUE_PROMPT}\n\nVisible Elements: {json.dumps(element_slice[:50])}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]
            )
            resp = llm.invoke([rescue_msg])
            payload = try_parse_json(resp.content) or {}

        summary_data = payload.get("summary", {"page_name": "Unknown", "domain_context": "SaaS", "available_actions": []})
        visible_elements = payload.get("locators", [])
        
        if isinstance(visible_elements, dict) and "visibleElements" in visible_elements:
             visible_elements = visible_elements["visibleElements"]

        result = {
            "url": url,
            "summary": summary_data,
            "locators": visible_elements
        }
        
        if visible_elements:
            cache[cache_key] = result
            cache_dir = os.path.dirname(cache_file)
            if cache_dir and not os.path.exists(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
            with open(cache_file, "w") as f:
                json.dump(cache, f, indent=2)
        else:
            print(colored("🛑 Mining result empty. Likely blocked by UI state or model refusal.", "red"))
            
        return result

    except Exception as e:
        print(colored(f"❌ Miner Error: {e}", "red"))
        return {"url": url, "summary": {}, "locators": []}

    except Exception as e:
        print(colored(f"❌ Miner Error: {e}", "red"))
        return {"url": url, "summary": {}, "locators": []}

if __name__ == "__main__":
    # For testing only
    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://saucedemo.com")
            res = await analyze_page(page, "https://saucedemo.com")
            print(json.dumps(res, indent=2))
            await browser.close()
    asyncio.run(main())
