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

    def navigate(self, url):
        self.page.goto(url, timeout=60000)
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name, project_name):
        take_screenshot(self.page, name, project_name)


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_field = self.page.locator("[data-test='username']")
        self.password_field = self.page.locator("[data-test='password']")
        self.login_button = self.page.locator("[data-test='login-button']")

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
        self.page.wait_for_url('**/inventory.html*', timeout=60000)


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_to_cart_backpack = self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
        self.add_to_cart_bike_light = self.page.locator("[data-test='add-to-cart-sauce-labs-bike-light']")
        self.cart_button = self.page.locator("a.shopping_cart_link")

    def add_item_to_cart(self, item_name):
        if item_name == 'Sauce Labs Backpack':
            self.add_to_cart_backpack.click()
        elif item_name == 'Sauce Labs Bike Light':
            self.add_to_cart_bike_light.click()
        else:
            raise ValueError(f"Item '{item_name}' not supported.")

    def go_to_cart(self):
        self.cart_button.click()
        self.page.wait_for_load_state("networkidle")


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.checkout_button = self.page.locator("[data-test='checkout']")

    def checkout(self):
        self.checkout_button.click()
        self.page.wait_for_load_state("networkidle")


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_field = self.page.locator("[data-test='firstName']")
        self.last_name_field = self.page.locator("[data-test='lastName']")
        self.postal_code_field = self.page.locator("[data-test='postalCode']")
        self.continue_button = self.page.locator("[data-test='continue']")

    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.postal_code_field.fill(postal_code)
        self.continue_button.click()
        self.page.wait_for_load_state("networkidle")


class CheckoutOverviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.finish_button = self.page.locator("[data-test='finish']")

    def finish_checkout(self):
        self.finish_button.click()
        self.page.wait_for_load_state("networkidle")


class CheckoutCompletePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.complete_header = self.page.locator(".complete-header")

    def get_complete_header_text(self):
        return self.complete_header.inner_text()


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    checkout_overview_page = CheckoutOverviewPage(page)
    checkout_complete_page = CheckoutCompletePage(page)

    # Navigate to the login page
    login_page.navigate("https://www.saucedemo.com/")

    # Login
    login_page.login("standard_user", "secret_sauce")

    # Add items to cart
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    # Go to cart
    inventory_page.go_to_cart()

    # Checkout
    cart_page.checkout()

    # Fill checkout information
    checkout_page.fill_checkout_info("John", "Doe", "12345")

    # Finish checkout
    checkout_overview_page.finish_checkout()

    # Verify checkout complete
    complete_header_text = checkout_complete_page.get_complete_header_text()
    assert complete_header_text == "Thank you for your order!"
    page.close()