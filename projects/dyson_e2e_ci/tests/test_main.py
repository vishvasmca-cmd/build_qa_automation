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

    def navigate(self, url, timeout=60000):
        try:
            self.page.goto(url, timeout=timeout)
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Navigation to {url} failed: {e}")
            project_name = os.getenv("PROJECT_NAME")
            take_screenshot(self.page, "navigation_error", project_name)
            raise

    def close_popup(self, popup_text):
        try:
            self.page.get_by_text(popup_text).click()
        except Exception as e:
            print(f"Popup closing failed: {e}")

    def wait_for_url(self, url, timeout=60000):
        self.page.wait_for_url(url, timeout=timeout)

    async def wait_for_stability(self, timeout=3000):
        await self.page.wait_for_timeout(timeout)


class HomePage:
    def __init__(self, page):
        self.page = page

    def search_product(self, product_name):
        self.page.get_by_placeholder(re.compile("Search products and parts", re.IGNORECASE)).fill(product_name)
        self.page.get_by_role("button", name=re.compile("Search products and parts", re.IGNORECASE)).click()

    def click_first_search_result(self, product_name):
        self.page.get_by_role("link", name=re.compile(product_name, re.IGNORECASE)).first().click()


class ProductPage:
    def __init__(self, page):
        self.page = page

    def add_to_cart(self):
        self.page.get_by_role("link", name=re.compile("Add to cart", re.IGNORECASE)).click()

    def go_to_checkout(self):
        self.page.get_by_role("link", name=re.compile("Checkout", re.IGNORECASE)).click()

    def verify_add_to_cart_button_visible(self):
        expect(self.page.get_by_role("link", name=re.compile("Add to cart", re.IGNORECASE))).to_be_visible()


def test_autonomous_flow(page):
    import sys, os
    sys.path.append(os.getcwd())
    try:
        from helpers import take_screenshot
    except Exception:
        def take_screenshot(page, name, project_name):
            page.screenshot(path=f"{name}.png")

    project_name = os.getenv("PROJECT_NAME")

    base_page = BasePage(page)
    home_page = HomePage(page)
    product_page = ProductPage(page)

    # 1. Handle Popup
    base_page.navigate("https://www.dyson.in/")
    base_page.close_popup("X")

    # 2. Search
    home_page.search_product("Dyson V15 Detect")
    page.wait_for_url("**/search*", timeout=60000)
    # Assuming the first search result contains the product name
    home_page.click_first_search_result("New Launch Dyson Airwrap\u2122 Origin multi-styler and dryer (Nic")
    page.wait_for_url("**/dyson-airwrap-multi-styler-origin-nickel-copper*", timeout=60000)

    # 3. PDP Verification
    product_page.verify_add_to_cart_button_visible()

    # 4. Cart Flow
    product_page.add_to_cart()
    page.wait_for_url("**/cart*", timeout=60000)

    # 5. Verification
    # Attempt to navigate to the cart page directly
    try:
        base_page.navigate("https://www.dyson.in/cart")
    except Exception as e:
        print(f"Navigation to cart failed: {e}")
        # If navigation to cart fails, try clicking the checkout button
        product_page.go_to_checkout()
        page.wait_for_url("**/checkout*", timeout=60000)

    base_page.wait_for_url("**/checkout*", timeout=60000)