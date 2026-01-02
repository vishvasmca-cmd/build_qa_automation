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
    path = os.path.join('projects/parabank_smart_flow/screenshots', f'{name}.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    page.screenshot(path=path)
    print(f'📸 Saved: {path}')

def test_autonomous_flow(page: Page):
    timestamp = random.randint(10000, 99999)
    username = f"user_{timestamp}"
    
    # timeout = 60000
    page.context.set_default_timeout(60000)
    # Generated for parabank_smart_flow
    page.goto("https://parabank.parasoft.com/parabank/register.htm")
    smart_action(page, "page.get_by_role(\"link\", name=\"Register\")", "click", None)
    take_screenshot(page, "step_0")
    expect(page).to_have_url(re.compile("register"))

    smart_action(page, "page.locator(\"input[name='customer.firstName']\")", "fill", "John")
    take_screenshot(page, "step_1")

    smart_action(page, "page.locator(\"input[name='customer.lastName']\")", "fill", "Doe")
    take_screenshot(page, "step_2")

    smart_action(page, "page.locator(\"input[name='customer.address.street']\")", "fill", "123 Main Street")
    take_screenshot(page, "step_3")

    smart_action(page, "page.locator(\"input[name='customer.address.city']\")", "fill", "New York")
    take_screenshot(page, "step_4")

    smart_action(page, "page.locator(\"input[name='customer.address.street']\")", "fill", "123 Main Street")
    take_screenshot(page, "step_5")

    smart_action(page, "page.locator(\"input[name='customer.address.state']\")", "fill", "NY")
    take_screenshot(page, "step_6")

    smart_action(page, "page.locator(\"input[name='customer.address.zipCode']\")", "fill", "10001")
    take_screenshot(page, "step_7")

    smart_action(page, "page.locator(\"input[name='customer.phoneNumber']\")", "fill", "555-1234")
    take_screenshot(page, "step_8")

    smart_action(page, "page.locator(\"input[name='customer.ssn']\")", "fill", "123-45-6789")
    take_screenshot(page, "step_9")

    smart_action(page, "page.locator(\"input[name='customer.username']\")", "fill", username)
    take_screenshot(page, "step_10")

    smart_action(page, "page.locator(\"input[name='repeatedPassword']\")", "fill", "Test@1234")
    take_screenshot(page, "step_11")

    smart_action(page, "page.locator(\"input[name='customer.password']\")", "fill", "Test@1234")
    take_screenshot(page, "step_12")

    smart_action(page, "page.locator(\"input[value='Register']\")", "click", None)
    take_screenshot(page, "step_13")
    expect(page.locator("body")).to_contain_text("Your account was created successfully", timeout=10000)

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_14")
    expect(page).to_have_url(re.compile("parabank/index"))

    smart_action(page, "page.get_by_role(\"link\", name=\"Open New Account\")", "click", None)
    take_screenshot(page, "step_15")
    expect(page).to_have_url(re.compile("openaccount"))

    smart_action(page, "page.locator(\"select\")", "click", None)
    take_screenshot(page, "step_16")

    smart_action(page, "page.locator(\"input[value='Open New Account']\")", "click", None)
    take_screenshot(page, "step_17")
    expect(page.locator("body")).to_contain_text("Account Opened!", timeout=10000)

    smart_action(page, "page.get_by_role(\"link\", name=\"Accounts Overview\")", "click", None)
    take_screenshot(page, "step_18")
    expect(page).to_have_url(re.compile("overview"))

    smart_action(page, "page.get_by_role(\"link\", name=\"Transfer Funds\")", "click", None)
    take_screenshot(page, "step_19")
    expect(page).to_have_url(re.compile("transfer"))

    smart_action(page, "page.locator(\"input[name='input']\")", "fill", "10")
    take_screenshot(page, "step_20")

    smart_action(page, "page.get_by_role(\"link\", name=\"Bill Pay\")", "click", None)
    take_screenshot(page, "step_21")
    expect(page).to_have_url(re.compile("billpay"))

    smart_action(page, "page.locator(\"input[name='payee.name']\")", "fill", "John Doe")
    take_screenshot(page, "step_22")

    smart_action(page, "page.locator(\"input[name='payee.address.street']\")", "fill", "123 Main Street")
    take_screenshot(page, "step_23")

    smart_action(page, "page.locator(\"input[name='payee.address.city']\")", "fill", "New York")
    take_screenshot(page, "step_24")

    smart_action(page, "page.locator(\"input[name='payee.address.state']\")", "fill", "NY")
    take_screenshot(page, "step_25")

    smart_action(page, "page.locator(\"input[name='payee.address.zipCode']\")", "fill", "10001")
    take_screenshot(page, "step_26")

    smart_action(page, "page.locator(\"input[name='payee.phoneNumber']\")", "fill", "555-1234")
    take_screenshot(page, "step_27")

    smart_action(page, "page.locator(\"input[name='payee.accountNumber']\")", "fill", "12345")
    take_screenshot(page, "step_28")

    smart_action(page, "page.locator(\"input[name='verifyAccount']\")", "fill", "12345")
    take_screenshot(page, "step_29")

    smart_action(page, "page.locator(\"input[name='amount']\")", "fill", "100")
    take_screenshot(page, "step_30")

    smart_action(page, "page.locator(\"input[value='Send Payment']\")", "click", None)
    take_screenshot(page, "step_31")
    expect(page.locator("body")).to_contain_text("Bill Payment Complete", timeout=10000)

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_32")

    smart_action(page, "page.get_by_role(\"link\", name=\"about\")", "click", None)
    take_screenshot(page, "step_33")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_34")

    smart_action(page, "page.get_by_role(\"link\", name=\"Open New Account\")", "click", None)
    take_screenshot(page, "step_35")

    smart_action(page, "page.get_by_role(\"link\", name=\"Accounts Overview\")", "click", None)
    take_screenshot(page, "step_36")

    smart_action(page, "page.get_by_role(\"link\", name=\"Open New Account\")", "click", None)
    take_screenshot(page, "step_37")

    smart_action(page, "page.get_by_role(\"link\", name=\"Accounts Overview\")", "click", None)
    take_screenshot(page, "step_38")

    smart_action(page, "page.get_by_role(\"link\", name=\"Open New Account\")", "click", None)
    take_screenshot(page, "step_39")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_40")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_41")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_42")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_43")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_44")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_45")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_46")

    smart_action(page, "page.get_by_role(\"link\", name=\"about\")", "click", None)
    take_screenshot(page, "step_47")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_48")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_49")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_50")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_51")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_52")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_53")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_54")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_55")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_56")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_57")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_58")

    smart_action(page, "page.get_by_role(\"link\", name=\"Home\")", "click", None)
    take_screenshot(page, "step_59")
    take_screenshot(page, "final_state")