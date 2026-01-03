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
You MUST prioritize `data-test` attributes for SauceDemo compatibility.

**MANDATORY OUTPUT FORMAT**:
{
  "visibleElements": [
    {
      "elementId": "el_0 (must match input)",
      "visibleText": "text",
      "role": "button",
      "dataTestId": "...",
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

**CRITICAL RULES FOR LOCATORS:**
1. **PYTHON SYNTAX ONLY**: Propose locators using Python snake_case (e.g., `get_by_role`, `get_by_test_id`).
2. **FORM FIELDS vs BUTTONS**: 
   - Text inputs, selects, textareas: Set role to "textbox" or "input". Include placeholder/name in visibleText.  
   - Submit buttons (type="submit" or value="Register"/"Submit"): Set role to "button". Mark with "ACTION_SUBMIT" in reason.
   - Regular buttons/links: Set role to "button" or "link".
3. If `customTestId` is present (from 'data-test'), you MUST propose: `page.locator("[data-test='VALUE']")`. 
4. If `testId` is present (from 'data-testid'), propose: `page.get_by_test_id("VALUE")`.
5. For inputs, prefer `page.locator("input[name='firstName']")` or by placeholder.
6. If using `get_by_role`, use keyword arguments: `page.get_by_role("button", name="Login")`.
7. **SHOPPING CART**: Ensure cart links are included in `visibleElements`.
9. **AVOID GENERIC**: Avoid generic selectors like `page.locator("button")`. Be specific.
10. **CONTEXT SCOPING**: If `context` field is present (e.g. "nav" or "footer"), PREPEND it to the locator for uniqueness.
    - Example: `page.locator('nav').locator('a[href="/signup"]')`
    - Example: `page.locator('footer').get_by_text("Contact")`

Output JSON only.
"""

SYSTEM_PROMPT_SUMMARY = """
You are a Website Analyst.
Given the text content and interactive elements of a page, provide:
1. `page_name`: Short name (e.g. "Login Page", "Registration Form", "Inventory List").
2. `domain_context`: What kind of app is this? (e.g. "E-commerce", "Banking", "SaaS").
3. `available_actions`: List of high-level actions user can take here (e.g. "Login", "Register new user", "Fill form fields", "Sort items").
4. `is_checkout_step`: Boolean.
5. `form_fields_detected`: If this is a form page, list field names you see (e.g., ["firstName", "lastName", "email", "password"]). Empty array if not a form.
6. `extracted_test_data`: Object containing any credentials or test data mentioned on the page (e.g., {"username": "tomsmith", "password": "SuperSecretPassword!"}). If none found, return empty object {}.

Output JSON only.
"""

async def extract_dom_snapshot(page: Page):
    """
    Extracts visible interactables and page text summary.
    """
    return await page.evaluate("""() => {
        const interactables = [];
        // Expanded selector to catch more interactive elements
        const selector = 'button, a, input:not([type=hidden]), select, textarea, [role="button"], [data-test], [data-testid], .shopping_cart_link';
        
        document.querySelectorAll(selector).forEach((el, index) => {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            
            if (rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none') {
                let testId = el.getAttribute('data-testid') || el.getAttribute('data-test-id') || '';
                let customTestId = el.getAttribute('data-test') || '';
                
                // Context Scoping Logic
                let context = '';
                try {
                    let parent = el.parentElement;
                    while (parent && parent !== document.body) {
                        if (parent.tagName) {
                            const tag = parent.tagName.toLowerCase();
                            if (['nav', 'footer', 'header', 'main', 'section'].includes(tag) || (parent.getAttribute && parent.getAttribute('role') === 'navigation')) {
                                context = tag;
                                // Add class/id specificity if available and simple
                                if (parent.id) context += `#${parent.id}`;
                                else if (parent.classList.length > 0) context += `.${parent.classList[0]}`;
                                break;
                            }
                        }
                        parent = parent.parentElement;
                    }
                } catch (e) {
                    // Ignore context errors
                }

                interactables.push({
                    id: `el_${index}`,
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    name: el.getAttribute('name') || '',
                    text: (el.innerText || el.textContent || '').slice(0, 50).replace(/\\n/g, ' ').trim(),
                    value: el.value || '', // Extract value for inputs
                    role: el.getAttribute('role') || '',
                    testId: testId,
                    customTestId: customTestId,
                    placeholder: el.getAttribute('placeholder') || '',
                    href: el.getAttribute('href') || '',
                    context: context
                });
            }
        });
        
        // Also get main page text for context
        const bodyText = (document.body && document.body.innerText) ? document.body.innerText.slice(0, 1000) : "";
        
        return { interactables, bodyText };
    }""")

async def analyze_page(page: Page, url: str, knowledge_context=None, cache_path="locator_cache.json", force_refresh=False):
    # 1. Extract DOM & Text
    data = await extract_dom_snapshot(page)
    raw_elements = data['interactables']
    body_text = data['bodyText']

    # Context string
    context_str = json.dumps(knowledge_context) if knowledge_context else "None"

    # 2. Check Cache
    cache_file = cache_path
    cache = {}
    if os.path.exists(cache_file) and not force_refresh:
        with open(cache_file, "r") as f:
            try: cache = json.load(f)
            except: pass
    
    structure_sig = "".join([f"{el['tag']}{el['text']}{el.get('testId','')}" for el in raw_elements])
    import hashlib
    content_hash = hashlib.md5(structure_sig.encode('utf-8')).hexdigest()
    cache_key = f"{url}_{content_hash}"
    
    if cache_key in cache:
        print(f"⚡ Using Cached Locators for: {url} (State Match)")
        cached_data = cache[cache_key]
        for i, cached_el in enumerate(cached_data['locators']):
            if i < len(raw_elements):
                cached_el['value'] = raw_elements[i].get('value', '')
        return cached_data

    print(f"🕵️  Mining Page via Vision+DOM: {url}")
    
    # 3. Capture Visual context
    screenshot_bytes = await page.screenshot(type="jpeg", quality=80) # Increased quality for better OCR
    import base64
    b64_img = base64.b64encode(screenshot_bytes).decode('utf-8')
    
    # 4. Single multi-modal call for both Summary and Locators
    element_slice = raw_elements[:150] # Increased for complex pages
    
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

    COMBINED_PROMPT = f"""
    URL: {url}
    Context: {context_str}
    Visible Elements: {json.dumps(element_slice)}
    
    {SYSTEM_PROMPT_SUMMARY}
    {SYSTEM_PROMPT_LOCATORS}
    
    **MANDATORY**: Return a valid JSON object.
    {{
      "summary": {{ "page_name": "...", "available_actions": [...] }},
      "locators": [ {{ "elementId": "...", "locatorCandidates": [...] }} ]
    }}
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
