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
        return self.page.get_by_role("link", name=" Products")

    @property
    def search_product_input(self):
        return self.page.locator("#search_product")

    @property
    def submit_search_button(self):
        return self.page.locator("#submit_search")

    @property
    def add_to_cart_button(self):
        return self.page.get_by_role("link", name="Add to cart")

    @property
    def continue_shopping_button(self):
        return self.page.get_by_role("button", name="Continue Shopping")

    @property
    def cart_link(self):
        return self.page.get_by_role("link", name="Cart")

    def navigate_to_products(self):
        self.products_link.click()
        self.page.wait_for_load_state("networkidle")

    def search_for_product(self, product_name):
        self.search_product_input.fill(product_name)
        self.page.locator("#submit_search").click()
        self.page.wait_for_load_state("networkidle")

    def add_product_to_cart(self, index):
        # Hover over the product card to make the 'Add to cart' button visible
        self.page.locator(".overlay-content").nth(index).hover()
        self.add_to_cart_button.nth(index).click()
        self.page.wait_for_load_state("networkidle")

    def continue_shopping(self):
        self.continue_shopping_button.click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_cart(self):
        self.cart_link.click()
        self.page.wait_for_load_state("networkidle")

class CartPage:
    def __init__(self, page):
        self.page = page

    @property
    def proceed_to_checkout_button(self):
        return self.page.get_by_role("link", name="Proceed To Checkout")

    def proceed_to_checkout(self):
        self.proceed_to_checkout_button.click()
        self.page.wait_for_load_state("networkidle")

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("domcontentloaded")

    # 2. Logic (using POM)
    products_page = ProductsPage(page)

    products_page.navigate_to_products()
    products_page.search_for_product("Dress")
    products_page.add_product_to_cart(0)
    products_page.continue_shopping()
    products_page.add_product_to_cart(1)
    products_page.continue_shopping()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()