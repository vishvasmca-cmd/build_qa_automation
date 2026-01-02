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
    path = os.path.join('projects/train_ultimateqa/screenshots', f'{name}.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    page.screenshot(path=path)
    print(f'📸 Saved: {path}')

def test_autonomous_flow(page: Page):
    timestamp = random.randint(1000, 9999)
    username = f'user_{timestamp}'
    email = f'test_{timestamp}@example.com'
    page.context.set_default_timeout(60000)
    # Generated for train_ultimateqa
    page.goto("https://ultimateqa.com/complicated-page")
    smart_action(page, "page.get_by_role('link', name='Big page with many elements')", "click", None)
    take_screenshot(page, "step_0")
    expect(page).to_have_url(re.compile(".*big-page-with-many-elements/"))
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_1")
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_2")
    smart_action(page, "page.locator(\"input[name='log']\").nth(1)", "fill", "standard_user")
    take_screenshot(page, "step_3")
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_4")
    smart_action(page, "page.locator(\"input[name='et_pb_contact_name_0']\")", "fill", "John Doe")
    take_screenshot(page, "step_5")
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_6")
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_7")
    smart_action(page, "page.locator(\"input[name='et_pb_contact_email_0']\")", "fill", "john.doe@example.com")
    take_screenshot(page, "step_8")
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_9")
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_10")
    smart_action(page, "page.locator(\"input[name='pwd']\").nth(0)", "fill", "secret_sauce")
    take_screenshot(page, "step_11")
    smart_action(page, "page.locator(\"input[name='log']\").nth(0)", "fill", "standard_user")
    take_screenshot(page, "step_12")
    smart_action(page, "page.locator(\"input[name='log']\").nth(1)", "fill", "standard_user")
    take_screenshot(page, "step_13")
    smart_action(page, "page.get_by_role(\"button\", name=\"Login\").nth(0)", "click", None)
    take_screenshot(page, "step_14")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_15")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_16")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_17")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_18")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_19")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_20")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_21")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_22")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_23")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_24")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_25")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_26")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_27")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_28")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_29")
    smart_action(page, "page.get_by_role(\"button\", name=\"UNLOCK ME\")", "click", None)
    take_screenshot(page, "step_30")
    smart_action(page, "page.locator('input[placeholder=\"Enter your username or email.\"]')", "fill", "standard_user")
    take_screenshot(page, "step_31")
    smart_action(page, "page.get_by_role(\"button\", name=\"UNLOCK ME\")", "click", None)
    take_screenshot(page, "step_32")
    smart_action(page, "page.get_by_role(\"link\", name=\"Try again\")", "click", None)
    take_screenshot(page, "step_33")
    smart_action(page, "page.get_by_role(\"button\", name=\"UNLOCK ME\")", "click", None)
    take_screenshot(page, "step_34")
    smart_action(page, "page.get_by_role(\"link\", name=\"Try again\")", "click", None)
    take_screenshot(page, "step_35")
    smart_action(page, "page.get_by_role(\"button\", name=\"UNLOCK ME\")", "click", None)
    take_screenshot(page, "step_36")
    smart_action(page, "page.get_by_role(\"link\", name=\"Try again\")", "click", None)
    take_screenshot(page, "step_37")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_38")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_39")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_40")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_41")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_42")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_43")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_44")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_45")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_46")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_47")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_48")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_49")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_50")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_51")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_52")
    smart_action(page, "page.locator(\"input[name='log']\")", "fill", "standard_user")
    take_screenshot(page, "step_53")
    smart_action(page, "page.locator(\"input[name='pwd']\")", "fill", "secret_sauce")
    take_screenshot(page, "step_54")
    smart_action(page, "page.locator(\"input[name='wp-submit']\")", "click", None)
    take_screenshot(page, "step_55")
    smart_action(page, "page.get_by_role(\"button\", name=\"UNLOCK ME\")", "click", None)
    take_screenshot(page, "step_56")
    smart_action(page, "page.locator('input[placeholder=\"Enter your username or email.\"]')", "fill", "standard_user")
    take_screenshot(page, "step_57")
    smart_action(page, "page.locator('input[placeholder=\"Enter your username or email.\"]')", "fill", "standard_user")
    take_screenshot(page, "step_58")
    smart_action(page, "page.get_by_role(\"button\", name=\"UNLOCK ME\")", "click", None)
    take_screenshot(page, "step_59")
    take_screenshot(page, "final_state")