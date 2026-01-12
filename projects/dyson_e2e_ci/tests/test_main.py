import sys
import os
sys.path.append(os.getcwd())

from playwright.sync_api import Page, expect
import re

try:
    from helpers import take_screenshot
except ImportError:
    def take_screenshot(page, name, project_name):
        pass  # Fallback if helpers not available

class HomePage:
    """Auto-generated Page Object for HomePage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def close_button(self):
        """The first step of the goal is to handle the popup. I will attempt to close the popup using the 'Clos"""
        return self.page.get_by_role("button", name="Close")

    @property
    def x_span(self):
        """The goal is to close the 'Subscribe' popup. The previous attempt to close the popup failed. Accordin"""
        return self.page.get_by_text("X")

    @property
    def search_products_and_parts_input(self):
        """The goal is to close the 'Subscribe' popup. The previous attempt to close the popup using the 'Close"""
        return self.page.get_by_placeholder("Search products and parts")

    @property
    def search_products_and_parts_button(self):
        """The goal is to search for 'Dyson V15 Detect' and click the first product result. I have already fill"""
        return self.page.get_by_label("Search products and parts")

    @property
    def click_element(self):
        """I am currently on the cart configuration page. The goal is to reach the checkout page. The next step"""
        return self.page.locator("body")

    @property
    def your_basket_has_1_items_in_it_link(self):
        """The goal is to reach the checkout page. The history shows that I have already added an item to the c"""
        return self.page.get_by_label("Your basket has 1 items in it")


class DysonIndiaPage:
    """Auto-generated Page Object for DysonIndiaPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def save_18_000_dyson_ontrac_cnc_c_link(self):
        """The goal is to search for 'Dyson V15 Detect' and click the first product result. I have already fill"""
        return self.page.get_by_role("link", name="Save ₹18,000 Dyson OnTrac™ (CNC Copper)   4.6 stars out of 5")


class ProductsPage:
    """Auto-generated Page Object for ProductsPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_to_cart_link(self):
        """The goal is to add the current product (Dyson OnTrac headphones) to the cart. The page context indic"""
        return self.page.get_by_role("link", name="Add to cart")

    @property
    def continue_to_basket_button(self):
        """The goal is to reach the checkout page. The previous steps were to close the popup, search for 'Dyso"""
        return self.page.get_by_role("button", name="Continue to basket")


def test_autonomous_flow(page: Page):
    """
    Workflow: 1. Handle Popup: Close 'Subscribe' popup. 2. Search: Search for 'Dyson V15 Detect' and click the first product result. 3. PDP Verification: Verify 'Add to Cart' button is visible. 4. Cart Flow: Click 'Add to Cart', verify cart drawer opens, and click 'Checkout'. 5. Verification: Ensure we reach the Checkout page.
    """
    # Navigate to target URL
    page.goto("https://www.dyson.in/")

    home_page = HomePage(page)
    dyson_india_page = DysonIndiaPage(page)
    products_page = ProductsPage(page)

    # Execute test steps
    # Step 0: The first step of the goal is to handle the popup. I will attempt to close the p
    home_page.close_button.click()

    # Step 1: The goal is to close the 'Subscribe' popup. The previous attempt to close the po
    home_page.x_span.click()

    # Step 2: The goal is to close the 'Subscribe' popup. The previous attempt to close the po
    home_page.search_products_and_parts_input.fill("Dyson V15 Detect")

    # Step 3: The goal is to search for 'Dyson V15 Detect' and click the first product result.
    home_page.search_products_and_parts_button.click()

    # Step 4: The goal is to search for 'Dyson V15 Detect' and click the first product result.
    dyson_india_page.save_18_000_dyson_ontrac_cnc_c_link.click()

    # Step 5: The goal is to add the current product (Dyson OnTrac headphones) to the cart. Th
    products_page.add_to_cart_link.click()

    # Step 6: The goal is to reach the checkout page. The previous steps were to close the pop
    products_page.continue_to_basket_button.click()

    # Step 7: I am currently on the cart configuration page. The goal is to reach the checkout
    home_page.click_element.click()

    # Step 8: The goal is to reach the checkout page. The previous steps involved adding an it
    home_page.search_products_and_parts_button.click()

    # Step 9: The goal is to complete the checkout flow. The history shows that I have already
    home_page.search_products_and_parts_button.click()

    # Step 10: The goal is to reach the checkout page. The history shows that I have already ad
    home_page.your_basket_has_1_items_in_it_link.click()
