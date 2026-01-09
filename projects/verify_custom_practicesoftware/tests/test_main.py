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
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name, project_name):
        take_screenshot(self.page, name, project_name)

class MyAccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate_to_my_account(self):
        self.page.get_by_role("link", name="My Account").click()

    def fill_registration_email(self, email):
        self.page.locator("#reg_email").fill(email)

    def fill_registration_password(self, password):
        self.page.locator("#reg_password").fill(password)

    def click_register(self):
        self.page.locator("[name='register']").click()

    def is_registration_error_visible(self):
        return self.page.locator(".woocommerce-error").is_visible()

    def get_registration_error_text(self):
        return self.page.locator(".woocommerce-error").inner_text()

def test_autonomous_flow(browser):
    page = browser.new_page()
    my_account_page = MyAccountPage(page)

    # Navigate to the base URL
    my_account_page.navigate("https://practice.automationtesting.in/")

    # Navigate to the My Account page
    my_account_page.navigate_to_my_account()

    # Fill the registration email
    my_account_page.fill_registration_email("test@example.com")

    # Fill the registration password
    my_account_page.fill_registration_password("password123")

    # Click the register button
    my_account_page.click_register()

    # Take a screenshot
    my_account_page.take_screenshot("registration_form", "AutomationPractice")

    page.wait_for_load_state("networkidle")

    # Check for error messages. If registration fails, there will be an error message.
    if my_account_page.is_registration_error_visible():
        print("Registration failed. Please check the error message.")
        error_message = my_account_page.get_registration_error_text()
        assert False, f"Registration Failed: {error_message}"
    else:
        print("Registration successful!")
