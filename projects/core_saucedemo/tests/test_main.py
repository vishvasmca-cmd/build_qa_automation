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


class LoginPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://www.saucedemo.com/")
        self.page.wait_for_load_state("networkidle")

    def login(self, username, password):
        self.page.locator("[data-test='username']").fill(username)
        self.page.locator("[data-test='password']").fill(password)
        self.page.locator("[data-test='login-button']").click()
        self.page.wait_for_load_state("networkidle")

class SaucedemoInventoryPage:
    def __init__(self, page):
        self.page = page

    @property
    def product_sort_dropdown(self):
        return self.page.locator("[data-test='product-sort-container']")

    def sort_by_price_low_to_high(self):
        self.product_sort_dropdown.select_option(label="Price (low to high)")
        self.page.wait_for_load_state("networkidle")

    def add_bike_light_to_cart(self):
        self.page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
        self.page.wait_for_load_state("networkidle")

    def go_to_cart(self):
        self.page.locator("[data-test='shopping-cart-link']").click()
        self.page.wait_for_load_state("networkidle")

class CartPage:
    def __init__(self, page):
        self.page = page

    def click_checkout(self):
        self.page.locator("[data-test='checkout']").click()
        self.page.wait_for_load_state("networkidle")

class CheckoutInformationPage:
    def __init__(self, page):
        self.page = page

    def fill_checkout_information(self, firstName, lastName, postalCode):
        self.page.locator("[data-test='firstName']").fill(firstName)
        self.page.locator("[data-test='lastName']").fill(lastName)
        self.page.locator("[data-test='postalCode']").fill(postalCode)
        self.page.locator("[data-test='continue']").click()
        self.page.wait_for_load_state("networkidle")

class CheckoutOverviewPage:
    def __init__(self, page):
        self.page = page

    def click_finish(self):
        self.page.locator("[data-test='finish']").click()
        self.page.wait_for_load_state("networkidle")

class CheckoutCompletePage:
    def __init__(self, page):
        self.page = page

    def click_back_to_products(self):
        self.page.locator("[data-test='back-to-products']").click()

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    login_page = LoginPage(page)
    inventory_page = SaucedemoInventoryPage(page)
    cart_page = CartPage(page)
    checkout_information_page = CheckoutInformationPage(page)
    checkout_overview_page = CheckoutOverviewPage(page)
    checkout_complete_page = CheckoutCompletePage(page)

    # 2. Logic (using POM)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.sort_by_price_low_to_high()
    inventory_page.add_bike_light_to_cart()
    inventory_page.go_to_cart()
    cart_page.click_checkout()
    checkout_information_page.fill_checkout_information("John", "Doe", "12345")
    checkout_overview_page.click_finish()
    #checkout_complete_page.click_back_to_products()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()