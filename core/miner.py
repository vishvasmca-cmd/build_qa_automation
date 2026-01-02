import asyncio
import json
import os
from playwright.async_api import async_playwright, Page
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

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
                
                interactables.push({
                    id: `el_${index}`,
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    name: el.getAttribute('name') || '',
                    text: el.innerText.slice(0, 50).replace(/\\n/g, ' ').trim(),
                    value: el.value || '', // Extract value for inputs
                    role: el.getAttribute('role') || '',
                    testId: testId,
                    customTestId: customTestId,
                    placeholder: el.getAttribute('placeholder') || '',
                    href: el.getAttribute('href') || ''
                });
            }
        });
        
        // Also get main page text for context
        const bodyText = document.body.innerText.slice(0, 1000);
        
        return { interactables, bodyText };
    }""")

async def analyze_page(page: Page, url: str, knowledge_context=None, cache_path="locator_cache.json", force_refresh=False):
    # Always extract DOM first to detect state changes
    data = await extract_dom_snapshot(page)
    raw_elements = data['interactables']
    body_text = data['bodyText']

    # Context string
    context_str = json.dumps(knowledge_context) if knowledge_context else "None"

    # Check Cache first
    cache_file = cache_path
    cache = {}
    if os.path.exists(cache_file) and not force_refresh:
        with open(cache_file, "r") as f:
            try:
                cache = json.load(f)
            except:
                pass
    
    # Generate Cache Key based on structural content (to handle state changes like Add -> Remove)
    # We use the list of tags + text to detect meaningful DOM changes
    structure_sig = "".join([f"{el['tag']}{el['text']}{el.get('testId','')}" for el in raw_elements])
    import hashlib
    content_hash = hashlib.md5(structure_sig.encode('utf-8')).hexdigest()
    cache_key = f"{url}_{content_hash}"
    
    if cache_key in cache:
        print(f"⚡ Using Cached Locators for: {url} (State Match)")
        cached_data = cache[cache_key]
        
        # KEY FIX: Update the 'value' property from live DOM to cached locators
        # We assume strict order match because hash matched
        for i, cached_el in enumerate(cached_data['locators']):
            if i < len(raw_elements):
                cached_el['value'] = raw_elements[i].get('value', '')
                
        return cached_data

    print(f"🕵️  Mining Page: {url} (New State)")
    
    # Capture Screenshot for Vision
    screenshot_bytes = await page.screenshot(type="jpeg", quality=50)
    import base64
    b64_img = base64.b64encode(screenshot_bytes).decode('utf-8')
    
    data = await extract_dom_snapshot(page)
    raw_elements = data['interactables']
    body_text = data['bodyText']
    
    # 1. Get Locators (Still Text-based is reliable for syntax, but we could add vision later)
    msg_locators = f"""
    URL: {url}
    Context/Knowledge: {context_str}
    Elements: {json.dumps(raw_elements[:75])}
    """
    
    def try_parse_json(content):
        content = content.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            match = re.search(r'(\{.*\})', content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except: pass
        return None

    import re
    resp_locators = llm.invoke([("system", SYSTEM_PROMPT_LOCATORS), ("human", msg_locators)])
    locator_data = try_parse_json(resp_locators.content)
    
    if not locator_data:
        print("⚠️ JSON Mining Failed. Retrying...")
        resp_locators = llm.invoke([("system", SYSTEM_PROMPT_LOCATORS), ("human", msg_locators)])
        locator_data = try_parse_json(resp_locators.content) or {"visibleElements": []}
    
    # 2. Get Summary (WITH VISION)
    # ...
    from langchain_core.messages import HumanMessage
    
    msg_summary = HumanMessage(
        content=[
            {"type": "text", "text": f"Analyze this page. URL: {url}\nKnowledge: {context_str}\nText Sample: {body_text}\nVisible Elements: {len(raw_elements)}"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
        ]
    )
    
    resp_summary = llm.invoke([("system", SYSTEM_PROMPT_SUMMARY), msg_summary])
    summary_data = try_parse_json(resp_summary.content) or {"page_name": "Unknown", "domain_context": "Unknown", "available_actions": []}
    
    # Handle occasional LLM drift where it returns list directly
    if isinstance(locator_data, list):
        visible_elements = locator_data
    else:
        visible_elements = locator_data.get("visibleElements", [])
    
    result = {
        "url": url,
        "summary": summary_data,
        "locators": visible_elements
    }
    
    # Save to Cache ONLY if we actually found locators
    if visible_elements:
        cache[cache_key] = result
        cache_dir = os.path.dirname(cache_file)
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(cache, f, indent=2)
    else:
        print("🛑 Mining result empty. Not caching.")
        
    return result

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
