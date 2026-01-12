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
        """The goal is to handle the popup, search for 'Dyson V15 Detect', verify the 'Add to Cart' button, pro"""
        return self.page.get_by_role("button", name="Close").first

    @property
    def x_span(self):
        """The goal is to close the 'Subscribe' popup. The previous attempt to close the popup failed. I will u"""
        return self.page.get_by_text("X").first

    @property
    def search_products_and_parts_input(self):
        """The goal is to close the 'Subscribe' popup. The previous action successfully closed a popup using th"""
        return self.page.get_by_placeholder("Search products and parts")

    @property
    def search_products_and_parts_button(self):
        """The goal is to search for 'Dyson V15 Detect'. I have already filled the search bar in the previous s"""
        return self.page.get_by_label("Search products and parts")

    @property
    def click_element(self):
        """The goal is to reach the checkout page. The current page is the cart page. The next step is to click"""
        return self.page.locator("body")

    @property
    def your_basket_has_1_items_in_it_link(self):
        """The goal is to reach the checkout page. The last action resulted in a chrome error, so I need to nav"""
        return self.page.get_by_label("Your basket has 1 items in it")


class DysonIndiaOfficialWebsitePage:
    """Auto-generated Page Object for DysonIndiaOfficialWebsitePage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def save_18_000_dyson_ontrac_cnc_c_link(self):
        """The goal is to search for 'Dyson V15 Detect' and click the first product result. I have already fill"""
        return self.page.get_by_role("link", name="Save ₹18,000 Dyson OnTrac™ (CNC Copper)   4.6 stars out of 5").first


class ProductsPage:
    """Auto-generated Page Object for ProductsPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_to_cart_link(self):
        """The goal is to add the current product (Dyson OnTrac headphones) to the cart, verify the cart drawer"""
        return self.page.get_by_role("link", name="Add to cart").first

    @property
    def continue_to_basket_button(self):
        """The goal is to verify the cart drawer opens and then click 'Checkout'. The previous action was addin"""
        return self.page.get_by_role("button", name="Continue to basket").first


class CartPage:
    """Auto-generated Page Object for CartPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def your_basket_has_1_items_in_it_link(self):
        """The goal is to reach the checkout page. The previous steps involved adding an item to the cart and v"""
        return self.page.get_by_label("Your basket has 1 items in it")


class CheckoutPage:
    """Auto-generated Page Object for CheckoutPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def continue_to_checkout_button(self):
        """The goal is to reach the checkout page. The current page is the cart page. The next step is to click"""
        return self.page.get_by_role("button", name="Continue to checkout").first


class UnknownPage:
    """Auto-generated Page Object for UnknownPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def done_element(self):
        """The goal is to complete the checkout process and reach the checkout page. The history shows that we """
        return self.page.locator("body")


def test_autonomous_flow(page: Page):
    """
    Workflow: 1. Handle Popup: Close 'Subscribe' popup. 2. Search: Search for 'Dyson V15 Detect' and click the first product result. 3. PDP Verification: Verify 'Add to Cart' button is visible. 4. Cart Flow: Click 'Add to Cart', verify cart drawer opens, and click 'Checkout'. 5. Verification: Ensure we reach the Checkout page.
    """
    # Navigate to target URL
    page.goto("https://www.dyson.in/")

    home_page = HomePage(page)
    dyson_india_official_website_page = DysonIndiaOfficialWebsitePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    unknown_page = UnknownPage(page)

    # Execute test steps
    # Step 0: The goal is to handle the popup, search for 'Dyson V15 Detect', verify the 'Add 
    home_page.close_button.click()

    # Step 1: The goal is to close the 'Subscribe' popup. The previous attempt to close the po
    home_page.x_span.click()

    # Step 2: The goal is to close the 'Subscribe' popup. The previous action successfully clo
    home_page.search_products_and_parts_input.fill("Dyson V15 Detect")

    # Step 3: The goal is to search for 'Dyson V15 Detect'. I have already filled the search b
    home_page.search_products_and_parts_button.click()

    # Step 4: The goal is to search for 'Dyson V15 Detect' and click the first product result.
    dyson_india_official_website_page.save_18_000_dyson_ontrac_cnc_c_link.click()

    # Step 5: The goal is to add the current product (Dyson OnTrac headphones) to the cart, ve
    products_page.add_to_cart_link.click()

    # Step 6: The goal is to verify the cart drawer opens and then click 'Checkout'. The previ
    products_page.continue_to_basket_button.click()

    # Step 7: The goal is to reach the checkout page. The current page is the cart page. The n
    home_page.click_element.click()

    # Step 8: The goal is to reach the checkout page. The last action resulted in a chrome err
    home_page.your_basket_has_1_items_in_it_link.click()

    # Step 9: The goal is to reach the checkout page. The previous steps involved adding an it
    cart_page.your_basket_has_1_items_in_it_link.click()

    # Step 10: The goal is to reach the checkout page. The current page is the cart page. The n
    checkout_page.continue_to_checkout_button.click()

    # Step 11: The goal is to complete the checkout process and reach the checkout page. The hi
    unknown_page.done_element.done()
