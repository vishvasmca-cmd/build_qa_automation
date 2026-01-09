# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/lib/templates')
from helpers import take_screenshot


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate_to_home(self):
        self.page.goto("https://automationexercise.com/")
        self.page.wait_for_load_state("networkidle")

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate_to_products_page(self):
        self.page.get_by_role("link", name="Products").click()
        self.page.wait_for_load_state("networkidle")

class ProductsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def search_product(self, product_name):
        self.page.locator("#search_product").fill(product_name)
        self.page.locator("#submit_search").click()
        self.page.wait_for_load_state("networkidle")

def test_autonomous_flow(browser):
    page = browser.new_page()
    home_page = HomePage(page)
    products_page = ProductsPage(page)

    home_page.navigate_to_home()
    home_page.navigate_to_products_page()
    products_page.search_product("Shirt")

    expect(page.locator(".productinfo").first).to_be_visible()