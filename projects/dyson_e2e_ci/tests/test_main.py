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
        """The goal is to close the 'Subscribe' popup, search for 'Dyson V15 Detect', verify the 'Add to Cart' """
        return self.page.get_by_role("button", name="Close").first()

    @property
    def x_span(self):
        """The goal is to close the 'Subscribe' popup. The previous attempt to close the popup failed. I will u"""
        return self.page.get_by_text("X").first()

    @property
    def search_products_and_parts_input(self):
        """The goal is to complete the user's workflow. The first step is to handle the popup. The previous act"""
        return self.page.get_by_placeholder("Search products and parts")

    @property
    def search_products_and_parts_button(self):
        """The goal is to search for 'Dyson V15 Detect'. I have already closed the popup and filled the search """
        return self.page.get_by_label("Search products and parts")

    @property
    def click_element(self):
        """The goal is to reach the checkout page. The history shows that I have already added an item to the c"""
        return self.page.locator("body")

    @property
    def your_basket_has_1_items_in_it_link(self):
        """The goal is to reach the checkout page. The last action was to click 'Continue to basket'. Now I nee"""
        return self.page.get_by_label("Your basket has 1 items in it")

    @property
    def search_button(self):
        """The goal is to reach the checkout page. The history shows that I have already added an item to the c"""
        return self.page.get_by_role("button", name="Search").first()


class DysonIndiaOfficialWebsitePage:
    """Auto-generated Page Object for DysonIndiaOfficialWebsitePage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def save_16_000_dyson_v8_absolute__link(self):
        """I have already closed the popup and searched for 'Dyson V15 Detect'. Now I need to click the first p"""
        return self.page.get_by_role("link", name="Save ₹16,000 Dyson V8 Absolute vacuum cleaner   4.4 stars ou").first()


class ProductsPage:
    """Auto-generated Page Object for ProductsPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_to_cart_link(self):
        """I am currently on the product detail page for 'Dyson V8 Absolute Vacuum'. The goal is to verify the """
        return self.page.get_by_role("link", name="Add to Cart").first()

    @property
    def continue_to_basket_button(self):
        """The goal is to reach the checkout page. The last action added an item to the cart. Now, I need to cl"""
        return self.page.get_by_role("button", name="Continue to basket").first()


def test_autonomous_flow(page: Page):
    """
    Workflow: 1. Handle Popup: Close 'Subscribe' popup. 2. Search: Search for 'Dyson V15 Detect' and click the first product result. 3. PDP Verification: Verify 'Add to Cart' button is visible. 4. Cart Flow: Click 'Add to Cart', verify cart drawer opens, and click 'Checkout'. 5. Verification: Ensure we reach the Checkout page.
    """
    # Navigate to target URL
    page.goto("https://www.dyson.in/")

    home_page = HomePage(page)
    dyson_india_official_website_page = DysonIndiaOfficialWebsitePage(page)
    products_page = ProductsPage(page)

    # Execute test steps
    # Step 0: The goal is to close the 'Subscribe' popup, search for 'Dyson V15 Detect', verif
    home_page.close_button.click()

    # Step 1: The goal is to close the 'Subscribe' popup. The previous attempt to close the po
    home_page.x_span.click()

    # Step 2: The goal is to complete the user's workflow. The first step is to handle the pop
    home_page.search_products_and_parts_input.fill("Dyson V15 Detect")

    # Step 3: The goal is to search for 'Dyson V15 Detect'. I have already closed the popup an
    home_page.search_products_and_parts_button.click()

    # Step 4: I have already closed the popup and searched for 'Dyson V15 Detect'. Now I need 
    dyson_india_official_website_page.save_16_000_dyson_v8_absolute__link.click()

    # Step 5: I am currently on the product detail page for 'Dyson V8 Absolute Vacuum'. The go
    products_page.add_to_cart_link.click()

    # Step 6: The goal is to reach the checkout page. The last action added an item to the car
    products_page.continue_to_basket_button.click()

    # Step 7: The goal is to reach the checkout page. The history shows that I have already ad
    home_page.click_element.click()

    # Step 8: The goal is to reach the checkout page. The last action was to click 'Continue t
    home_page.your_basket_has_1_items_in_it_link.click()

    # Step 9: The goal is to reach the checkout page. The last action was clicking 'Your baske
    home_page.search_products_and_parts_button.click()

    # Step 10: The goal is to reach the checkout page. The last action was to click the 'Search
    home_page.search_products_and_parts_input.fill("Dyson V15 Detect")

    # Step 11: The goal is to reach the checkout page. The previous steps involved adding an it
    home_page.search_products_and_parts_button.click()

    # Step 12: The goal is to reach the checkout page. The previous steps involved adding an it
    home_page.search_products_and_parts_input.click()

    # Step 13: The goal is to reach the checkout page. The previous steps involved searching fo
    home_page.search_products_and_parts_input.fill("Dyson V15 Detect")

    # Step 14: The goal is to reach the checkout page. The previous steps involved searching fo
    home_page.your_basket_has_1_items_in_it_link.click()

    # Step 15: The goal is to reach the checkout page. The history shows that I have already ad
    home_page.your_basket_has_1_items_in_it_link.click()

    # Step 16: The goal is to reach the checkout page. The history shows that I have already ad
    home_page.search_button.click()
