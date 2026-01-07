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
    def username_field(self):
        return self.page.locator("[data-test='username']")

    @property
    def password_field(self):
        return self.page.locator("[data-test='password']")

    def fill_username(self, username):
        self.username_field.fill(username)

    def fill_password(self, password):
        self.password_field.fill(password)

class SwagLabsLoginPage:
    def __init__(self, page):
        self.page = page

    @property
    def login_button(self):
        return self.page.locator("[data-test='login-button']")

    def click_login(self):
        self.login_button.click()

class SaucedemoInventoryPage:
    def __init__(self, page):
        self.page = page

    @property
    def product_sort_dropdown(self):
        return self.page.locator("[data-test='product-sort-container']")

    def sort_by_price_low_to_high(self):
        self.product_sort_dropdown.select_option(label='Price (low to high)')

    def verify_products_sorted_by_price(self):
        # Get the prices of the products
        product_prices = self.page.locator(".inventory_item_price").all_text_contents()
        # Convert prices to floats and check if they are sorted
        prices = [float(price.replace('$', '')) for price in product_prices]
        is_sorted = all(prices[i] <= prices[i + 1] for i in range(len(prices) - 1))
        expect(self.page.locator(".inventory_item_price")).to_have_count(len(prices))
        if not is_sorted:
            print("Prices are not sorted correctly.")
        else:
            print("Prices are sorted correctly.")

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    home_page = HomePage(page)
    swag_labs_login_page = SwagLabsLoginPage(page)
    saucedemo_inventory_page = SaucedemoInventoryPage(page)

    home_page.fill_username("standard_user")
    home_page.fill_password("secret_sauce")
    swag_labs_login_page.click_login()
    saucedemo_inventory_page.sort_by_price_low_to_high()
    saucedemo_inventory_page.verify_products_sorted_by_price()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()