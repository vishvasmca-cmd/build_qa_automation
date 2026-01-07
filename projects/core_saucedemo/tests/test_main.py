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

    def goto(self):
        self.page.goto("https://www.saucedemo.com/")
        self.page.wait_for_load_state("networkidle")

    def fill_username(self, username):
        self.page.locator("[data-test='username']").fill(username)

    def fill_password(self, password):
        self.page.locator("[data-test='password']").fill(password)

class SwagLabsLoginPage:
    def __init__(self, page):
        self.page = page

    def click_login(self):
        self.page.locator("[data-test='login-button']").click()

class SaucedemoInventoryPage:
    def __init__(self, page):
        self.page = page

    @property
    def product_sort_container(self):
        return self.page.locator("[data-test='product-sort-container']")

    def sort_by_price_low_to_high(self):
        self.product_sort_container.select_option(label="Price (low to high)")

    def add_bike_light_to_cart(self):
        self.page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home_page = HomePage(page)
    login_page = SwagLabsLoginPage(page)
    inventory_page = SaucedemoInventoryPage(page)

    # 2. Logic (using POM)
    home_page.goto()
    expect(page).to_have_url("https://www.saucedemo.com/")
    home_page.fill_username("standard_user")
    home_page.fill_password("secret_sauce")
    login_page.click_login()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    inventory_page.sort_by_price_low_to_high()
    inventory_page.add_bike_light_to_cart()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()