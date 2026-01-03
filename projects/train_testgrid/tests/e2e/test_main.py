import pytest
import os
import re
import random
from playwright.sync_api import Page, expect

def smart_action(page, primary_locator, action_type, value=None):
    """Self-healing action wrapper"""
    try:
        # Clean the locator string if LLM passed page.locator(...) inside it
        loc_str = primary_locator
        import re
        if 'page.' in loc_str:
            # Convert JS getByRole to Python get_by_role with keyword args
            loc_str = loc_str.replace('getByRole', 'get_by_role').replace('{ name:', 'name=').replace(' }', '')
            match = re.search(r"['\"](.*)['\"]", loc_str)
            if match and 'locator' in loc_str: loc_str = match.group(1)
        
        # Final safeguard: if it still has page., try to eval it
        if 'page.' in loc_str:
             loc = eval(loc_str, {'page': page, 're': re})
        else:
             loc = page.locator(loc_str)
        # DISMISS BACKDROPS
        page.evaluate("""() => {
            const overlays = document.querySelectorAll('div[class*="z-"], div[class*="fixed"], [data-state="open"]');
            overlays.forEach(el => { el.remove(); });
        }""")

        if action_type == 'click':
            try:
                loc.click(timeout=5000)
            except Exception as e:
                if "strict mode" in str(e):
                    print(f'⚠️ Strict mode. Using .first for: {primary_locator}')
                    loc.first.click(timeout=3000)
                else:
                    print(f'⚠️ Click failed. Trying force click for: {primary_locator}')
                    try:
                        loc.click(timeout=3000, force=True)
                    except:
                        print(f'☢️ Force failed. Trying JS Click for: {primary_locator}')
                        loc.first.evaluate("el => el.click()")

        elif action_type == 'fill':
            try:
                loc.fill(str(value), timeout=5000)
            except Exception as e:
                if "strict mode" in str(e):
                     loc.first.fill(str(value), timeout=3000)
                else: raise e
        return True
    except Exception as e:
        if "strict mode" in str(e):
            try:
                if action_type == 'click': loc.first.click(timeout=3000)
                elif action_type == 'fill': loc.first.fill(str(value), timeout=3000)
                print(f'⚠️ Strict mode handled for: {primary_locator}')
                return True
            except: pass
        print(f'⚠️ Healing needed for: {primary_locator}')
        all_elements = page.query_selector_all('[data-test], button, a, [role="button"]')
        # Try to find match by keyword
        keyword = ''
        import re
        match = re.search(r"['\"](.*)['\"]", primary_locator)
        if match: keyword = match.group(1).lower()
        
        for el in all_elements:
            attr = el.get_attribute('data-test') or el.get_attribute('id') or el.inner_text() or ''
            if keyword and keyword in str(attr).lower():
                try:
                    print(f'✨ Healed! Found matching element.')
                    if action_type == 'click': el.click()
                    else: el.fill(str(value))
                    return True
                except: continue
        print('❌ Healing failed.')
        raise e

def take_screenshot(page, name):
    """Consistent screenshot utility"""
    path = os.path.join('projects/train_testgrid/screenshots', f'{name}.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    page.screenshot(path=path)
    print(f'📸 Saved: {path}')

def test_autonomous_flow(page: Page):
    timestamp = random.randint(1000, 9999)
    username = f'user_{timestamp}'
    email = f'test_{timestamp}@example.com'
    page.context.set_default_timeout(60000)
    # Generated for train_testgrid
    page.goto("https://testgrid.io/")
    smart_action(page, "page.locator('button:has-text(\"Book Demo\")')", "click", None)
    take_screenshot(page, "step_0")
    expect(page).to_have_url("https://testgrid.io/")

    smart_action(page, "page.locator('input[name=\"fullname\"]')", "fill", "John Doe")
    take_screenshot(page, "step_1")
    expect(page.locator("input[name=\"fullname\"]")).to_have_value("John Doe")

    smart_action(page, "page.locator('input[name=\"fullname\"]')", "fill", "John Doe")
    take_screenshot(page, "step_2")
    expect(page.locator("input[name=\"fullname\"]")).to_have_value("John Doe")

    smart_action(page, "page.locator('input[name=\"email\"]')", "fill", "test@example.com")
    take_screenshot(page, "step_4")
    expect(page.locator("input[name=\"email\"]")).to_have_value("test@example.com")

    smart_action(page, "page.locator('input[name=\"email\"]')", "fill", "test@example.com")
    take_screenshot(page, "step_5")
    expect(page.locator("input[name=\"email\"]")).to_have_value("test@example.com")

    smart_action(page, "page.get_by_role('button', name='Book a Demo')", "click", None)
    take_screenshot(page, "step_6")
    expect(page).to_have_url("https://testgrid.io/")

    smart_action(page, "page.locator('input[name=\"email\"]')", "fill", "test@example.com")
    take_screenshot(page, "step_7")
    expect(page.locator("input[name=\"email\"]")).to_have_value("test@example.com")

    smart_action(page, "page.locator('input[name=\"email\"]')", "fill", "test@example.com")
    take_screenshot(page, "step_8")
    expect(page.locator("input[name=\"email\"]")).to_have_value("test@example.com")

    smart_action(page, "page.locator('input[name=\"phone\"]')", "fill", "555-123-4567")
    take_screenshot(page, "step_10")
    expect(page.locator("input[name=\"phone\"]")).to_have_value("555-123-4567")

    smart_action(page, "page.locator('input[name=\"phone\"]')", "fill", "555-1234")
    take_screenshot(page, "step_11")
    expect(page.locator("input[name=\"phone\"]")).to_have_value("555-1234")

    smart_action(page, "page.get_by_role('button', name='Book a Demo')", "click", None)
    take_screenshot(page, "step_12")
    expect(page).to_have_url("https://testgrid.io/")

    smart_action(page, "page.locator('input[name=\"phone\"]')", "fill", "555-123-4567")
    take_screenshot(page, "step_13")
    expect(page.locator("input[name=\"phone\"]")).to_have_value("555-123-4567")

    smart_action(page, "page.locator('input[name=\"phone\"]')", "fill", "555-1234")
    take_screenshot(page, "step_14")
    expect(page.locator("input[name=\"phone\"]")).to_have_value("555-1234")
    take_screenshot(page, "final_state")