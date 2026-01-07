# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/templates')
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

    def search_product(self, product_name):
        self.products_link.click()
        self.search_product_input.fill(product_name)
        self.submit_search_button.click()

    def add_to_cart(self):
        self.page.get_by_role("link", name="Add to cart").click()

    def continue_shopping(self):
        self.page.get_by_role("button", name="Continue Shopping").click()

    def close_ad(self):
        try:
            self.page.get_by_text('Close ad').click()
        except:
            pass

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    products_page = ProductsPage(page)
    
    # Step 0: Click Products link
    products_page.products_link.click()
    
    #Step 1 and 2: Close Ad if present (handling potential ad)
    products_page.close_ad()

    # Step 3: Click Products link again to ensure correct page state after ad close
    products_page.products_link.click()

    # Step 4: Fill search product input
    products_page.search_product("Blue Top")

    # Step 6: Add to cart
    products_page.add_to_cart()

    # Step 7: Continue Shopping
    products_page.continue_shopping()

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()