# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
from helpers import take_screenshot, wait_for_stability


class ProductsPage:
    def __init__(self, page):
        self.page = page

    @property
    def products_link(self):
        return self.page.get_by_role("link", name=re.compile("Products", re.IGNORECASE))

    @property
    def search_product_input(self):
        return self.page.locator("#search_product")

    def search_product(self, product_name):
        self.search_product_input.fill(product_name)


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://automationexercise.com/")
    wait_for_stability(page)

    # 2. Logic (using POM)
    products_page = ProductsPage(page)
    products_page.products_link.click()
    page.wait_for_url("**/products")
    wait_for_stability(page)
    expect(products_page.search_product_input).to_be_visible()
    products_page.search_product("Dress")

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()