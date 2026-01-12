# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append(os.getcwd())
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


async def wait_for_stability(page, timeout=2000):
    last_content = await page.content()
    while True:
        await page.wait_for_timeout(500)
        current_content = await page.content()
        if current_content == last_content:
            break
        last_content = current_content

class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url, timeout=60000)
        self.page.wait_for_load_state()

    def close_popup(self):
        try:
            self.page.locator('button[aria-label="Close"]', has_text=re.compile("close", re.IGNORECASE)).click()
        except Exception as e:
            print(f"Popup not found or could not be closed: {e}")

    def search_product(self, product_name):
        self.page.get_by_placeholder(re.compile("Search products and parts", re.IGNORECASE)).fill(product_name)
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_timeout(500)
        # self.page.wait_for_load_state()

class HomePage:
    def __init__(self, page):
        self.page = page

    def click_first_search_result(self):
        # Assuming the first search result is a link or button with the product name
        # This locator might need adjustment based on the actual HTML structure
        self.page.locator("div[class*='ProductGrid'] a").first().click()


class ProductDetailPage:
    def __init__(self, page):
        self.page = page

    def add_to_cart(self):
        self.page.get_by_role("button", name=re.compile("Add to cart", re.IGNORECASE)).click()

    def verify_add_to_cart_button_visible(self):
        expect(self.page.get_by_role("button", name=re.compile("Add to cart", re.IGNORECASE))).to_be_visible()

class CartPage:
    def __init__(self, page):
        self.page = page

    def checkout(self):
        self.page.get_by_role("link", name=re.compile("Checkout", re.IGNORECASE)).click()
        # self.page.wait_for_load_state()

    def verify_cart_drawer_opens(self):
        # Assuming there's a specific element that indicates the cart drawer is open
        # This locator needs to be adjusted based on the actual HTML structure
        expect(self.page.locator(".cart-drawer")).to_be_visible()

class CheckoutPage:
    def __init__(self, page):
        self.page = page

    def verify_checkout_page(self):
        # Assuming there's a specific element that indicates the checkout page is open
        # This locator needs to be adjusted based on the actual HTML structure
        expect(self.page.url).to_contain("/checkout")


def test_autonomous_flow(page):
    import sys, os
    sys.path.append(os.getcwd())
    try:
        from helpers import take_screenshot
    except ImportError:
        def take_screenshot(page, name, project_name):
            print(f"Screenshot skipped: {name}")
            pass

    project_name = os.getenv('PROJECT_NAME', 'Dyson')

    base_page = BasePage(page)
    home_page = HomePage(page)
    product_detail_page = ProductDetailPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    # 1. Navigate to the Dyson India website
    base_page.navigate("https://www.dyson.in/")
    take_screenshot(page, "home_page", project_name)

    # 2. Handle the popup
    base_page.close_popup()

    # 3. Search for 'Dyson V15 Detect'
    base_page.search_product("Dyson V15 Detect")
    take_screenshot(page, "search_results", project_name)

    # 4. Click the first product result
    home_page.click_first_search_result()
    page.wait_for_url("**/en-IN/products/**")
    take_screenshot(page, "product_detail_page", project_name)

    # 5. PDP Verification: Verify 'Add to Cart' button is visible
    product_detail_page.verify_add_to_cart_button_visible()

    # 6. Cart Flow: Click 'Add to Cart'
    product_detail_page.add_to_cart()
    take_screenshot(page, "add_to_cart", project_name)

    # 7. Verify cart drawer opens
    cart_page.verify_cart_drawer_opens()

    # 8. Click 'Checkout'
    cart_page.checkout()
    page.wait_for_url("**/checkout/**")

    # 9. Verification: Ensure we reach the Checkout page
    checkout_page.verify_checkout_page()
