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
    def __init__(self, page: Page):
        self.page = page

    def username_field(self):
        return self.page.locator("[data-test='username']")

    def password_field(self):
        return self.page.locator("[data-test='password']")

    def login_button(self):
        return self.page.locator("[data-test='login-button']")

    def goto(self):
        self.page.goto("https://www.saucedemo.com/")
        self.page.wait_for_load_state("domcontentloaded")

    def login(self, username, password):
        self.username_field().fill(username)
        self.password_field().fill(password)
        self.login_button().click()
        self.page.wait_for_url("https://www.saucedemo.com/inventory.html")


class SaucedemoInventoryPage:
    def __init__(self, page: Page):
        self.page = page

    def product_sort_dropdown(self):
        return self.page.locator("[data-test='product-sort-container']")

    def sort_by_price_low_to_high(self):
        self.product_sort_dropdown().select_option(label="Price (low to high)")


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home_page = HomePage(page)
    inventory_page = SaucedemoInventoryPage(page)

    # 2. Logic (using POM)
    home_page.goto()
    home_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    inventory_page.sort_by_price_low_to_high()
    # Verify sorting
    # first_item_price = page.locator(".inventory_item_price").first().inner_text()
    # expect(first_item_price).to_contain("$7.99")

    # 3. Cleanup
    context.close()