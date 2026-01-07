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


class SignupLoginPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://automationexercise.com/login")
        self.page.wait_for_load_state("networkidle")

    @property
    def signup_login_link(self):
        return self.page.get_by_role("link", name="Signup / Login")

    @property
    def signup_name_input(self):
        return self.page.locator("form[action='/signup'] [name='name']")

    @property
    def signup_email_input(self):
        return self.page.locator("form[action='/signup'] [name='email']")

    @property
    def signup_button(self):
        return self.page.get_by_role("button", name="Signup")

    @property
    def password_input(self):
        return self.page.locator("#password")

    @property
    def first_name_input(self):
        return self.page.locator("#first_name")

    @property
    def last_name_input(self):
        return self.page.locator("#last_name")

    def signup(self, name, email, password, first_name, last_name):
        self.signup_login_link.click()
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()
        self.password_input.fill(password)
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    signup_login_page = SignupLoginPage(page)
    signup_login_page.goto()

    # 2. Logic (using POM)
    signup_login_page.signup(
        name="Stress Tester",
        email="stress_test_unique@gmail.com",
        password="12345",
        first_name="Stress",
        last_name="Test",
    )

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()