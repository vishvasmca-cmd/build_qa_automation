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


class HomePage:
    def __init__(self, page):
        self.page = page

    @property
    def products_link(self):
        return self.page.get_by_role("link", name="\ue8f8 Products")

    @property
    def subscribe_email_input(self):
        return self.page.locator("#susbscribe_email")

    def navigate_to_products(self):
        self.products_link.click()
        self.page.wait_for_load_state("networkidle")

class ProductsPage:
    def __init__(self, page):
        self.page = page

    @property
    def search_product_input(self):
        return self.page.locator("#search_product")

    @property
    def submit_search_button(self):
        return self.page.locator("#submit_search")

    @property
    def add_to_cart_button_locator(self):
        return self.page.get_by_role("link", name="Add to cart")

    @property
    def cart_link(self):
        return self.page.get_by_role("link", name="Cart")

    def search_for_product(self, product_name):
        self.search_product_input.fill(product_name)
        self.submit_search_button.click()
        self.page.wait_for_load_state("networkidle")

    def add_to_cart_button(self, product_name):
        # The previous implementation was failing because the overlay was intercepting the click.
        # This implementation uses a more specific locator to target the add to cart button within the product overlay.
        return self.page.locator(".product-overlay").filter(has_text=product_name).locator("a").filter(has_text="Add to cart").first

    def navigate_to_cart(self):
        self.cart_link.click()
        self.page.wait_for_load_state("networkidle")

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("domcontentloaded")

    # 2. Logic (using POM)
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    # Navigate to Products page
    home_page.navigate_to_products()

    # Search for 'Dress'
    products_page.search_for_product("Dress")

    # Add the first dress to cart
    products_page.add_to_cart_button("Dress").click()

    # Navigate to cart
    products_page.navigate_to_cart()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()