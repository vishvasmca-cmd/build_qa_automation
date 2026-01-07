# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
from helpers import take_screenshot


class ProductsPage:
    def __init__(self, page):
        self.page = page

    @property
    def products_link(self):
        return self.page.get_by_role("link", name="\ue8f8 Products")

    @property
    def search_product_input(self):
        return self.page.locator("#search_product")

    @property
    def submit_search_button(self):
        return self.page.locator("#submit_search")

    def add_to_cart_button(self, index: int = 0):
        return self.page.get_by_role("link", name="Add to cart").nth(index)

    @property
    def continue_shopping_button(self):
        return self.page.get_by_role("button", name="Continue Shopping")

    @property
    def cart_link(self):
        return self.page.get_by_role("link", name="Cart")

    def navigate_to_products(self):
        self.products_link.click()

    def search_product(self, product_name: str):
        self.search_product_input.fill(product_name)

    def add_product_to_cart(self, index: int = 0):
        self.add_to_cart_button(index).click(force=True)

    def continue_shopping(self):
        self.continue_shopping_button.click()

    def navigate_to_cart(self):
        self.cart_link.click()


class CartPage:
    def __init__(self, page):
        self.page = page

    @property
    def proceed_to_checkout_link(self):
        return self.page.get_by_role("link", name="Proceed To Checkout")

    def proceed_to_checkout(self):
        self.proceed_to_checkout_link.click()


class LoginPage:
    def __init__(self, page):
        self.page = page

    @property
    def register_login_link(self):
        return self.page.get_by_role("link", name="Register / Login")

    def navigate_to_login(self):
        self.register_login_link.click()


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    login_page = LoginPage(page)

    # Navigate to Products page
    products_page.navigate_to_products()

    # Search for 'Dress'
    products_page.search_product("Dress")

    # Add a dress to the cart (first one)
    products_page.add_product_to_cart()

    # Continue shopping
    products_page.continue_shopping()

    # Navigate to cart
    products_page.navigate_to_cart()

    # Proceed to checkout
    cart_page.proceed_to_checkout()

    # Handle login/register
    login_page.navigate_to_login()

    # Navigate to Products page again
    products_page.navigate_to_products()

    # Search for 'Dress' again
    products_page.search_product("Dress")

    # Add a dress to the cart (first one)
    products_page.add_product_to_cart()

    # Add another dress to the cart (second one)
    products_page.add_product_to_cart(index=1)

    # Add another dress to the cart (third one)
    products_page.add_product_to_cart(index=2)

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()