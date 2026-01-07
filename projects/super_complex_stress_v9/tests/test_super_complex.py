import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/templates')
from helpers import wait_for_stability


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("https://automationexercise.com/")

    @property
    def products_link(self):
        return self.page.get_by_role("link", name="Products")

    def navigate_to_products(self):
        self.products_link.click()
        self.page.wait_for_url("**/products")
        wait_for_stability(self.page)


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_product_input(self):
        return self.page.locator("#search_product")

    def search_product(self, product_name):
        self.search_product_input.fill(product_name)
        self.search_product_input.press("Enter")
        wait_for_stability(self.page)


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)



def test_autonomous_flow(page: Page, home_page: HomePage, products_page: ProductsPage):
    # 1. Setup (using fixtures)

    # 2. Logic (using POM)
    home_page.goto()
    home_page.navigate_to_products()
    products_page.search_product("Blue Top")
    expect(page.locator(".productinfo", has_text="Blue Top")).to_be_visible()

    # 3. Cleanup (Playwright handles context and page closing)
