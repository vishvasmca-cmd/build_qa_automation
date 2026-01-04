import pytest
import os
import re
import random
from playwright.sync_api import Page, expect

def wait_for_stability(page):
    """Ensures page is stable before interaction"""
    try:
        page.wait_for_load_state('domcontentloaded', timeout=5000)
        page.wait_for_load_state('networkidle', timeout=3000)
    except: pass
    # Check for blocking overlays
    page.evaluate("""() => {
        const overlays = document.querySelectorAll('.modal.show, .modal-backdrop.show, .overlay, [role="dialog"]');
        overlays.forEach(el => {
            if (window.getComputedStyle(el).display !== 'none') {
                console.log('Found overlay, waiting/hiding:', el);
                // el.style.display = 'none'; // Optional: Aggressively hide if needed
            }
        });
    }""")

def smart_action(page, primary_locator, action_type, value=None):
    """Robust, Self-Healing Action Wrapper"""
    wait_for_stability(page)
    loc = None
    try:
        # 1. Parsing Locator
        loc_str = primary_locator
        import re
        if 'page.' in loc_str:
            loc_str = loc_str.replace('getByRole', 'get_by_role').replace('{ name:', 'name=').replace(' }', '')
            match = re.search(r"['\"](.*?)['\"]", loc_str)
            if match and 'locator' in loc_str: loc_str = match.group(1)
            if 'page.' in loc_str: loc = eval(loc_str, {'page': page, 're': re})
        
        if not loc: loc = page.locator(loc_str)
    
        # 2. Pre-Action Checks
        if not loc.count() and 'strict mode' not in action_type:
            # Try relaxed visibility
            pass
        
        # 3. Execution
        if action_type == 'click':
            try:
                loc.click(timeout=5000)
            except Exception as e:
                print(f'⚠️ Standard click failed: {e}. Trying force.')
                try:
                    loc.click(timeout=3000, force=True)
                except:
                    # Last resort: JS Click
                    print(f'☢️ JS Click needed for: {primary_locator}')
                    loc.first.evaluate('el => el.click()')
        
        elif action_type == 'fill':
            loc.fill(str(value), timeout=5000)
        
        return True
    
    except Exception as e:
        # 4. Self-Healing Fallback
        print(f'🚑 Healing needed for: {primary_locator} ({e})')
        try:
            # Fallback 1: Text approximations
            keyword = ''
            match = re.search(r"['\"](.*?)['\"]", primary_locator)
            if match: keyword = match.group(1).lower()
            
            if keyword:
                healed = page.get_by_role('button', name=re.compile(keyword, re.IGNORECASE))
                if healed.count():
                    print('✨ Healed via Role/Name match!')
                    if action_type == 'click': healed.first.click()
                    else: healed.first.fill(str(value))
                    return True
        except: pass
        
        print('❌ Action failed after healing attempts.')
        raise e

def take_screenshot(page, name):
    """Consistent screenshot utility"""
    path = os.path.join('projects/parabank_regression/screenshots', f'{name}.png')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    page.screenshot(path=path)
    print(f'📸 Saved: {path}')

def test_autonomous_flow(page: Page):
    timestamp = random.randint(1000, 9999)
    username = f'user_{timestamp}'
    email = f'test_{timestamp}@example.com'
    page.context.set_default_timeout(60000)
    # Generated for parabank_regression
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    # Step 0
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name='username']").fill("standard_user")
    expect(page.locator("input[name='username']")).to_have_value("standard_user")

    # Step 1
    page.locator("input[name='password']").fill("secret_sauce")
    expect(page.locator("input[name='password']")).to_have_value("secret_sauce")

    # Step 2
    page.get_by_role("button", name="Log In").click()
    # Cannot assert URL change as per rule #1

    # Step 3
    page.locator("input[value='Log In']").click()
    # Cannot assert URL change as per rule #1

    # Step 4
    page.locator("input[name='username']").fill("standard_user")
    expect(page.locator("input[name='username']")).to_have_value("standard_user")

    # Step 5
    page.locator("input[name='password']").fill("secret_sauce")
    expect(page.locator("input[name='password']")).to_have_value("secret_sauce")

    # Step 6
    page.locator("input[value='Log In']").click()
    # Cannot assert URL change as per rule #1

    # Step 7
    page.locator("input[name='username']").fill("standard_user")
    expect(page.locator("input[name='username']")).to_have_value("standard_user")

    # Step 8
    page.locator("input[name='password']").fill("secret_sauce")
    expect(page.locator("input[name='password']")).to_have_value("secret_sauce")

    # Step 9
    page.locator("input[name='password']").fill("secret_sauce")
    expect(page.locator("input[name='password']")).to_have_value("secret_sauce")

    # Step 11
    page.get_by_role("link", name="Register").click()
    # Cannot assert URL change as per rule #1

    # Step 12
    page.locator("input[name='customer.firstName']").fill("John")
    expect(page.locator("input[name='customer.firstName']").to_have_value("John"))

    # Step 13
    page.locator("input[name='customer.lastName']").fill("Doe")
    expect(page.locator("input[name='customer.lastName']").to_have_value("Doe"))

    # Step 14
    page.locator("input[name='customer.address.street']").fill("123 Main Street")
    expect(page.locator("input[name='customer.address.street']").to_have_value("123 Main Street"))

    # Step 15
    page.locator("input[name='customer.address.city']").fill("New York")
    expect(page.locator("input[name='customer.address.city']").to_have_value("New York"))

    # Step 16
    page.locator("input[name='customer.address.state']").fill("NY")
    expect(page.locator("input[name='customer.address.state']").to_have_value("NY"))

    # Step 17
    page.locator("input[name='customer.address.city']").fill("New York")
    expect(page.locator("input[name='customer.address.city']").to_have_value("New York"))

    # Step 18
    page.locator("input[name='customer.address.zipCode']").fill("10001")
    expect(page.locator("input[name='customer.address.zipCode']").to_have_value("10001"))

    # Step 19
    page.locator("input[name='customer.phoneNumber']").fill("555-1234")
    expect(page.locator("input[name='customer.phoneNumber']").to_have_value("555-1234"))

    # Step 20
    page.locator("input[name='customer.ssn']").fill("123-45-6789")
    expect(page.locator("input[name='customer.ssn']").to_have_value("123-45-6789"))

    # Step 21
    page.locator("input[name='customer.username']").fill("user_4383")
    expect(page.locator("input[name='customer.username']").to_have_value("user_4383"))

    # Step 22
    page.locator("input[name='customer.password']").fill("Test@1234")
    expect(page.locator("input[name='customer.password']").to_have_value("Test@1234"))

    # Step 23
    page.locator("input[name='repeatedPassword']").fill("Test@1234")
    expect(page.locator("input[name='repeatedPassword']").to_have_value("Test@1234"))

    # Step 24
    page.get_by_role("button", name="Register").click()
    # Cannot assert URL change as per rule #1

    # Step 25
    page.get_by_role("link", name="Open New Account").click()
    # Cannot assert URL change as per rule #1

    # Step 26
    page.get_by_role("button", name="Open New Account").click()
    # Cannot assert URL change as per rule #1

    # Step 27
    page.get_by_role("link", name="Transfer Funds").click()
    # Cannot assert URL change as per rule #1

    # Step 28
    page.locator("input[name='input']").fill("10")
    expect(page.locator("input[name='input']").to_have_value("10"))

    # Step 29
    page.locator("input[value='Transfer']").click()
    # Cannot assert URL change as per rule #1

    # Step 30
    page.locator('a[href="billpay.htm"]').click()
    # Cannot assert URL change as per rule #1

    # Step 31
    page.locator("input[name='payee.name']").fill("Electric Company")
    expect(page.locator("input[name='payee.name']").to_have_value("Electric Company"))

    # Step 32
    page.locator("input[name='payee.address.street']").fill("123 Main Street")
    expect(page.locator("input[name='payee.address.street']").to_have_value("123 Main Street"))

    # Step 33
    page.locator("input[name='payee.address.city']").fill("New York")
    expect(page.locator("input[name='payee.address.city']").to_have_value("New York"))

    # Step 34
    page.locator("input[name='payee.address.state']").fill("NY")
    expect(page.locator("input[name='payee.address.state']").to_have_value("NY"))

    # Step 35
    page.locator("input[name='payee.address.zipCode']").fill("10001")
    expect(page.locator("input[name='payee.address.zipCode']").to_have_value("10001"))

    # Step 36
    page.locator("input[name='payee.phoneNumber']").fill("555-1234")
    expect(page.locator("input[name='payee.phoneNumber']").to_have_value("555-1234"))

    # Step 37
    page.locator("input[name='payee.accountNumber']").fill("12345")
    expect(page.locator("input[name='payee.accountNumber']").to_have_value("12345"))

    # Step 38
    page.locator("input[name='verifyAccount']").fill("12345")
    expect(page.locator("input[name='verifyAccount']").to_have_value("12345"))

    # Step 39
    page.locator("input[name='amount']").fill("100")
    expect(page.locator("input[name='amount']").to_have_value("100"))

    # Step 40
    page.locator("input[value='Send Payment']").click()
    expect(page.locator("body")).to_contain_text("Bill Payment Complete")

    # Step 41
    page.get_by_role("link", name="Log Out").click()
    expect(page.locator("body")).to_contain_text("Customer Login")
    take_screenshot(page, "final_state")