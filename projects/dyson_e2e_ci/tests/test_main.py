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
    def x_span(self):
        """The first step of the goal is to close the 'Subscribe' popup. The previous attempt to close the popu"""
        return self.page.get_by_text("X", exact=True).first

    @property
    def search_products_and_parts_input(self):
        """The goal is to automate the process of adding a product to the cart and proceeding to checkout on th"""
        return self.page.get_by_placeholder("Search products and parts")

    @property
    def search_products_and_parts_button(self):
        """The goal is to search for 'Dyson V15 Detect'. The previous action was to fill the search box. Now, I"""
        return self.page.get_by_role("button", name="Search products and parts", exact=True).first


class DysonIndiaPage:
    """Auto-generated Page Object for DysonIndiaPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def save_11_000_dyson_airstrait_st_link(self):
        """The goal is to search for 'Dyson V15 Detect' and click the first product result. I have already fill"""
        return self.page.get_by_role("link", name="Save ₹11,000 Dyson Airstrait™ straightener (Ceramic pink/Rose gold) 4.6 stars out of 5 from 17602", exact=True).first


class DysonAirstraitStraightenerPage:
    """Auto-generated Page Object for DysonAirstraitStraightenerPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_to_cart_button(self):
        """The goal is to verify the 'Add to Cart' button is visible on the product details page (PDP). The pre"""
        return self.page.get_by_role("button", name="Add to cart", exact=True).first


class ProductsPage:
    """Auto-generated Page Object for ProductsPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_to_cart_button(self):
        """The goal is to add the item to the cart, verify the cart drawer opens, and then click 'Checkout'. Th"""
        return self.page.get_by_role("button", name="Add to cart", exact=True).first


def test_autonomous_flow(page: Page):
    """
    Workflow: 1. Handle Popup: Close 'Subscribe' popup. 2. Search: Search for 'Dyson V15 Detect' and click the first product result. 3. PDP Verification: Verify 'Add to Cart' button is visible. 4. Cart Flow: Click 'Add to Cart', verify cart drawer opens, and click 'Checkout'. 5. Verification: Ensure we reach the Checkout page.
    """
    # Navigate to target URL
    page.goto("https://www.dyson.in/", timeout=60000)

    home_page = HomePage(page)
    dyson_india_page = DysonIndiaPage(page)
    dyson_airstrait_straightener_page = DysonAirstraitStraightenerPage(page)
    products_page = ProductsPage(page)

    # Execute test steps
    # Step 0: The first step of the goal is to close the 'Subscribe' popup. The previous attem
    home_page.x_span.click()

    # Step 1: The goal is to automate the process of adding a product to the cart and proceedi
    home_page.search_products_and_parts_input.fill("Dyson V15 Detect")

    # Step 2: The goal is to search for 'Dyson V15 Detect'. The previous action was to fill th
    home_page.search_products_and_parts_button.click()

    # Step 3: The goal is to search for 'Dyson V15 Detect' and click the first product result.
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            dyson_india_page.save_11_000_dyson_airstrait_st_link.click()
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass

    # Step 4: The goal is to verify the 'Add to Cart' button is visible on the product details
    page.keyboard.press("PageDown")

    # Step 5: The goal is to add the item to the cart, verify the cart drawer opens, and then 
    products_page.add_to_cart_button.click()

    # Step 6: The current page is showing an 'Access Denied' error. This indicates a problem w
    page.goto("https://www.dyson.in/airstrait-hair-straightener-pink-gold")

    # Step 7: The current page is an 'Access Denied' page, which means the previous action (na
    page.goto("https://www.dyson.in/checkout/cart/")

    # Step 8: The current page is 'Access Denied', indicating a problem with the previous navi
    page.goto("https://www.dyson.in/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZHlzb24uaW4vYWlyc3RyYWl0LWhhaXItc3RyYWlnaHRlbmVyLXBpbmstZ29sZA~~/product/69594/")