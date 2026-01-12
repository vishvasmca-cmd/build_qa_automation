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
    def laptops_link(self):
        """The goal is to complete the purchase flow. The first step is to click on the 'Laptops' category. The"""
        return self.page.get_by_role("link", name="Laptops", exact=True).first

    @property
    def sony_vaio_i5_link(self):
        """The goal is to complete the purchase flow. The first step is to click on the 'Laptops' category. Thi"""
        return self.page.get_by_role("link", name="Sony vaio i5", exact=True).first


class DemoblazePage:
    """Auto-generated Page Object for DemoblazePage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def sony_vaio_i5_link(self):
        """The goal is to complete the purchase flow. The first step is to click on the 'Laptops' category. Thi"""
        return self.page.get_by_role("link", name="Sony vaio i5", exact=True).first


class ProductDetailsSonyVaioI5Page:
    """Auto-generated Page Object for ProductDetailsSonyVaioI5Page"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_to_cart_link(self):
        """The goal is to complete the purchase flow. I have already clicked on 'Laptops' and 'Sony vaio i5'. N"""
        return self.page.get_by_role("link", name="Add to cart", exact=True).first


class CartPage:
    """Auto-generated Page Object for CartPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def cart_link(self):
        """The goal is to complete the purchase flow. I have already added the item to the cart and accepted th"""
        return self.page.get_by_role("link", name="Cart", exact=True).first

    @property
    def place_order_button(self):
        """I am currently on the cart page. The next step in the goal is to click 'Place Order'."""
        return self.page.get_by_role("button", name="Place Order", exact=True).first

    @property
    def country_input(self):
        """The goal is to complete the purchase flow. I'm currently on the cart page, and I have already clicke"""
        return self.page.locator("#country")

    @property
    def city_input(self):
        """The goal is to complete the purchase flow. I'm currently on the cart page and have filled the countr"""
        return self.page.locator("#city")

    @property
    def credit_card_input(self):
        """I am currently on the cart page, and I have already filled in the 'Country' and 'City' fields. The n"""
        return self.page.locator("#card")


def test_autonomous_flow(page: Page):
    """
    Workflow: 1. Search/Filter: Click 'Laptops' category. 2. Selection: Click on 'Sony vaio i5'. 3. Action: Click 'Add to cart' and accept the alert. 4. Checkout: Go to 'Cart', click 'Place Order', fill 'Name' and 'Credit card' in the modal, and click 'Purchase'.
    """
    # Navigate to target URL
    page.goto("https://www.demoblaze.com/")

    home_page = HomePage(page)
    demoblaze_page = DemoblazePage(page)
    product_details_sony_vaio_i5_page = ProductDetailsSonyVaioI5Page(page)
    cart_page = CartPage(page)

    # Execute test steps
    # Step 0: The goal is to complete the purchase flow. The first step is to click on the 'La
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            home_page.laptops_link.click()
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass

    # Step 1: The goal is to complete the purchase flow. The first step is to click on the 'La
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            home_page.sony_vaio_i5_link.click()
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass

    # Step 2: The goal is to complete the purchase flow. The first step is to click on the 'La
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            demoblaze_page.sony_vaio_i5_link.click()
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass

    # Step 3: The goal is to complete the purchase flow. I have already clicked on 'Laptops' a
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            product_details_sony_vaio_i5_page.add_to_cart_link.click()
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass

    # Step 4: The goal is to complete the purchase flow. I have already added the item to the 
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            cart_page.cart_link.click()
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass

    # Step 5: I am currently on the cart page. The next step in the goal is to click 'Place Or
    cart_page.place_order_button.click()

    # Step 6: The goal is to complete the purchase flow. I'm currently on the cart page, and I
    cart_page.country_input.fill("test")

    # Step 7: The goal is to complete the purchase flow. I'm currently on the cart page and ha
    cart_page.city_input.fill("Test City")

    # Step 8: I am currently on the cart page, and I have already filled in the 'Country' and 
    cart_page.credit_card_input.fill("1234567890")
