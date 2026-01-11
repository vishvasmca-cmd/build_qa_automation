# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
# Dynamic path discovery: Find root of 'inner-event' and append core path
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to project root (e.g., projects/name/tests/ -> inner-event)
# We assume tests are usually in projects/<name>/tests/ or projects/<name>/tests/e2e
root_dir = current_dir
for _ in range(10): # Max depth search
    if os.path.exists(os.path.join(root_dir, 'core')):
        break
    parent = os.path.dirname(root_dir)
    if parent == root_dir: break
    root_dir = parent

sys.path.append(os.path.join(root_dir, 'core', 'lib', 'templates'))
try:
    from helpers import take_screenshot
except ImportError:
    # Fallback for different structures
    sys.path.append(os.path.abspath(os.path.join(current_dir, '../../../../core/lib/templates')))
    from helpers import take_screenshot



class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
        # self.page.wait_for_load_state("networkidle") # Too strict for some sites

    def take_screenshot(self, name):
        self.page.screenshot(path=f"{name}.png")

    def close_popup(self):
        try:
            self.page.locator("#onesignal-slidedown-cancel-button").click(timeout=5000)
        except Exception:
            print("Popup did not appear or could not be closed.")




class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def search_product(self, product_name):
        # 1. Click search icon to expand (if needed)
        try:
            # Common patterns for search triggers
            search_trigger = self.page.get_by_role("button", name=re.compile("search", re.IGNORECASE)).first
            if search_trigger.is_visible():
                search_trigger.click()
                self.page.wait_for_timeout(500) # Animation wait
        except:
             print("Search trigger click failed or not found, trying input directly.")

        # 2. Find the ENABLED input
        inputs = self.page.get_by_placeholder(re.compile("Search products and parts", re.IGNORECASE))
        count = inputs.count()
        found = False
        for i in range(count):
            if inputs.nth(i).is_visible() and inputs.nth(i).is_enabled():
                inputs.nth(i).fill(product_name)
                inputs.nth(i).press("Enter")
                found = True
                break
        
        if not found:
             # Fallback
             inputs.first.fill(product_name)
             inputs.first.press("Enter")

    def click_first_product(self, product_name):
        self.page.get_by_role("link", name=re.compile(product_name, re.IGNORECASE)).first.click()


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def add_to_cart(self):
        self.page.get_by_role("link", name=re.compile("Add to cart", re.IGNORECASE)).click()

    def continue_to_basket(self):
        self.page.locator("#product-updatecart-button").click()

    def go_to_checkout(self):
        self.page.get_by_text(re.compile("Checkout", re.IGNORECASE)).click()
        self.page.wait_for_url("**/checkout*", timeout=60000)


def test_autonomous_flow(page: Page):
    import sys, os
    sys.path.append(os.getcwd())
    try:
        from helpers import take_screenshot
    except ImportError:
        def take_screenshot(page, name, project_name):
            print(f"Screenshot skipped: {name}")
            pass

    # page = browser.new_page() -> REMOVED, use fixture
    base_page = BasePage(page)
    home_page = HomePage(page)
    product_page = ProductPage(page)

    # 1. Navigate to the home page
    base_page.navigate("https://www.dyson.in/")

    # Handle Popup
    base_page.close_popup()

    # 3. Search for a product
    home_page.search_product("Dyson V15 Detect")

    # 4. Click the first product
    home_page.click_first_product("Dyson V15 Detect")

    # 5. Add the product to the cart
    product_page.add_to_cart()

    # 6. Continue to basket
    product_page.continue_to_basket()

    # 7. Go to checkout
    product_page.go_to_checkout()

    # 8. Verification: Ensure we reach the Checkout page.
    expect(page).to_have_url(re.compile(r"checkout", re.IGNORECASE))
