# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/templates')
from helpers import wait_for_stability, smart_action, take_screenshot


class HomePage:
    def __init__(self, page):
        self.page = page

    @property
    def register_link(self):
        return self.page.get_by_role("link", name="Register")

    def navigate_to_registration(self):
        smart_action(self.page, self.register_link, "click")
        wait_for_stability(self.page)

class RegistrationPage:
    def __init__(self, page):
        self.page = page

    @property
    def first_name_input(self):
        return self.page.locator("#customer.firstName")

    @property
    def password_input(self):
        return self.page.locator("[name='password']")

    def fill_first_name(self, first_name):
        smart_action(self.page, self.first_name_input, "fill", value=first_name)
        wait_for_stability(self.page)

    def fill_password(self, password):
        smart_action(self.page, self.password_input, "fill", value=password)
        wait_for_stability(self.page)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    wait_for_stability(page)

    # 2. Logic (using POM)
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.navigate_to_registration()
    registration_page.fill_first_name("user2636")
    registration_page.fill_password("user2636")

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()