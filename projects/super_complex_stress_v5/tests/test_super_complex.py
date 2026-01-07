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


class ProductPage:
    def __init__(self, page):
        self.page = page

    @property
    def products_link(self):
        return self.page.get_by_role("link", name="\ue8f8 Products")

    @property
    def search_product_input(self):
        return self.page.locator("#search_product")

    @property
    def add_to_cart_link(self):
        return self.page.get_by_role("link", name="Add to cart")

    @property
    def continue_shopping_button(self):
        return self.page.get_by_role("button", name="Continue Shopping")

    @property
    def submit_search_button(self):
        return self.page.locator("#submit_search")

    def navigate_to_products(self):
        self.page.goto("https://automationexercise.com/")
        self.products_link.click()
        self.page.wait_for_load_state("networkidle")

    def search_product(self, product_name):
        self.search_product_input.fill(product_name)
        self.submit_search_button.click()
        self.page.wait_for_load_state("networkidle")

    def add_product_to_cart(self):
        self.page.locator("div.product-overlay").first().hover()
        self.page.locator("div.product-overlay").first().locator("a", has_text="Add to cart").click()
        self.page.wait_for_load_state("networkidle")

    def continue_shopping(self):
        self.continue_shopping_button.click()
        self.page.wait_for_load_state("networkidle")

class CheckoutPage:
    def __init__(self, page):
        self.page = page

    @property
    def cart_link(self):
        return self.page.get_by_role("link", name="Cart")

    @property
    def proceed_to_checkout_link(self):
        return self.page.get_by_role("link", name="Proceed To Checkout")

    def navigate_to_cart(self):
        self.cart_link.click()
        self.page.wait_for_load_state("networkidle")

    def proceed_to_checkout(self):
        self.proceed_to_checkout_link.click()
        self.page.wait_for_load_state("networkidle")

class LoginPage:
    def __init__(self, page):
        self.page = page

    @property
    def register_login_link(self):
        return self.page.get_by_role("link", name="Register / Login")

    @property
    def name_input(self):
        return self.page.locator("[name='name']")

    @property
    def email_input(self):
        return self.page.locator("[name='email']")

    @property
    def signup_button(self):
        return self.page.get_by_role("button", name="Signup")

    def navigate_to_login(self):
        self.register_login_link.click()
        self.page.wait_for_load_state("networkidle")

    def enter_name(self, name):
        self.name_input.fill(name)

    def enter_email(self, email):
        self.email_input.fill(email)

    def click_signup(self):
        self.signup_button.click()
        self.page.wait_for_load_state("networkidle")

class SignupPage:
    def __init__(self, page):
        self.page = page

    @property
    def password_input(self):
        return self.page.locator("#password")

    @property
    def first_name_input(self):
        return self.page.locator("#first_name")

    def enter_password(self, password):
        self.password_input.fill(password)

    def enter_first_name(self, first_name):
        self.first_name_input.fill(first_name)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    product_page = ProductPage(page)
    checkout_page = CheckoutPage(page)
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    # Step 0, 1, 2: Navigate to products page
    product_page.navigate_to_products()

    # Step 3: Search for 'Blue Top'
    product_page.search_product("Blue Top")

    # Step 4: Add 'Blue Top' to cart
    product_page.add_product_to_cart()

    # Step 5: Continue Shopping
    product_page.continue_shopping()

    # Step 6: Search for 'Men Tshirt'
    product_page.search_product("Men Tshirt")

    # Step 7: Add 'Men Tshirt' to cart
    product_page.add_product_to_cart()

    # Step 8: Search for 'Sleeveless Dress'
    product_page.search_product("Sleeveless Dress")

    # Step 9 & 10: Add 'Sleeveless Dress' to cart & submit search
    product_page.add_product_to_cart()

    # Step 11: Navigate to cart
    checkout_page.navigate_to_cart()

    # Step 12: Proceed to checkout
    checkout_page.proceed_to_checkout()

    # Step 13: Navigate to Register / Login
    login_page.navigate_to_login()

    # Step 14: Fill name
    login_page.enter_name("Stress Tester")

    # Step 15: Fill email
    login_page.enter_email("stress_test_unique@gmail.com")

    # Step 16: Click signup
    login_page.click_signup()

    # Step 17, 18: Fill password
    signup_page.enter_password("12345")

    # Step 19: Fill first name
    signup_page.enter_first_name("Stress")

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()