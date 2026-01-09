# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/lib/templates')
from helpers import take_screenshot


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def take_screenshot(self, name, project_name):
        take_screenshot(self.page, name, project_name)

    def wait_for_load_state(self, state='networkidle'):
        self.page.wait_for_load_state(state=state)


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


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.product_sort_dropdown = self.page.locator("[data-test='product-sort-container']")

    def sort_products(self, order):
        self.product_sort_dropdown.select_option(order)

    def add_to_cart(self, item_name):
        self.page.locator(".inventory_item").filter(has_text=item_name).locator("button:has-text('Add to cart')").click()

    def go_to_item_details(self, item_name):
        self.page.locator(".inventory_item").filter(has_text=item_name).locator(".inventory_item_name").click()


class ItemDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def go_back(self):
        self.page.go_back()


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def go_to_checkout(self):
        self.page.locator("[data-test='checkout']").click()


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_field = self.page.locator("[data-test='firstName']")
        self.last_name_field = self.page.locator("[data-test='lastName']")
        self.postal_code_field = self.page.locator("[data-test='postalCode']")
        self.continue_button = self.page.locator("[data-test='continue']")

    def fill_info(self, first_name, last_name, postal_code):
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.postal_code_field.fill(postal_code)

    def click_continue(self):
        self.continue_button.click()


class CheckoutOverviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.finish_button = self.page.locator("[data-test='finish']")

    def click_finish(self):
        self.finish_button.click()


class CheckoutCompletePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.back_home_button = self.page.locator("[data-test='back-to-products']")

    def go_back_home(self):
        self.back_home_button.click()


class Header(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.logout_link = self.page.locator("#logout_sidebar_link")
        self.cart_link = self.page.locator(".shopping_cart_link")
        self.burger_menu = self.page.locator("#react-burger-menu-btn")

    def logout(self):
        self.burger_menu.click()
        self.logout_link.click()

    def go_to_cart(self):
        self.cart_link.click()


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    item_details_page = ItemDetailsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    checkout_overview_page = CheckoutOverviewPage(page)
    checkout_complete_page = CheckoutCompletePage(page)
    header = Header(page)

    try:
        # Login
        login_page.navigate("https://www.saucedemo.com/")
        login_page.login("standard_user", "secret_sauce")
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        login_page.wait_for_load_state()

        # Sort Z-A
        inventory_page.sort_products("za")
        inventory_page.wait_for_load_state()

        # Add 'Test.allTheThings() T-Shirt'
        inventory_page.add_to_cart("Test.allTheThings() T-Shirt")
        inventory_page.wait_for_load_state()

        # Go to item details 'Sauce Labs Onesie'
        inventory_page.go_to_item_details("Sauce Labs Onesie")
        inventory_page.wait_for_load_state()

        # go back
        item_details_page.go_back()
        item_details_page.wait_for_load_state()

        # Add 'Sauce Labs Bike Light'
        inventory_page.add_to_cart("Sauce Labs Bike Light")
        inventory_page.wait_for_load_state()

        # Go to Cart
        header.go_to_cart()
        expect(page).to_have_url("https://www.saucedemo.com/cart.html")
        header.wait_for_load_state()

        # Checkout
        cart_page.go_to_checkout()
        expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
        cart_page.wait_for_load_state()

        # Info 'Jane' 'Doe' '12345'
        checkout_page.fill_info("Jane", "Doe", "12345")
        checkout_page.click_continue()
        expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
        checkout_page.wait_for_load_state()

        # Finish
        checkout_overview_page.click_finish()
        expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
        checkout_overview_page.wait_for_load_state()

        # Back Home
        checkout_complete_page.go_back_home()
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        checkout_complete_page.wait_for_load_state()

        # Logout
        header.logout()
        expect(page).to_have_url("https://www.saucedemo.com/")
        header.wait_for_load_state()

    except Exception as e:
        login_page.take_screenshot("test_failed", "saucedemo")
        raise e

