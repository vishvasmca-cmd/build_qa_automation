import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append(r'C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/templates')
from helpers import wait_for_stability, smart_action, take_screenshot


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def username_field(self):
        return self.page.locator("[data-test='username']")

    def password_field(self):
        return self.page.locator("[data-test='password']")

    def login_button(self):
        return self.page.locator("[data-test='login-button']")

    def goto(self) -> None:
        self.page.goto("https://www.saucedemo.com/")
        wait_for_stability(self.page)

    def login(self, username: str, password: str) -> None:
        self.page.locator("[data-test='username']").fill(username)
        self.page.locator("[data-test='password']").fill(password)
        self.page.locator("[data-test='login-button']").click()
        wait_for_stability(self.page)


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def product_sort_dropdown(self):
        return self.page.locator("[data-test='product-sort-container']")

    def add_to_cart_backpack_button(self):
        return self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']")

    def sort_products(self) -> None:
        self.page.locator("[data-test='product-sort-container']").click()
        wait_for_stability(self.page)

    def add_backpack_to_cart(self) -> None:
        self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
        wait_for_stability(self.page)


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    # 2. Logic
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.sort_products()
    inventory_page.add_backpack_to_cart()

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()