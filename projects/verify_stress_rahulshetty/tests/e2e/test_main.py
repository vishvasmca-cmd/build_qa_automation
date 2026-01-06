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


class RegistrationPage:
    def __init__(self, page):
        self.page = page

    @property
    def register_here_link(self):
        return self.page.get_by_role("link", name="Register here")

    @property
    def first_name_field(self):
        return self.page.locator("#firstName")

    @property
    def last_name_field(self):
        return self.page.locator("#lastName")

    @property
    def user_email_field(self):
        return self.page.locator("#userEmail")

    def navigate_to_registration(self):
        smart_action(self.page, self.register_here_link, "click")
        wait_for_stability(self.page)

    def fill_first_name(self, first_name):
        smart_action(self.page, self.first_name_field, "fill", value=first_name)
        wait_for_stability(self.page)

    def fill_last_name(self, last_name):
        smart_action(self.page, self.last_name_field, "fill", value=last_name)
        wait_for_stability(self.page)

    def fill_email(self, email):
        smart_action(self.page, self.user_email_field, "fill", value=email)
        wait_for_stability(self.page)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/client/#/auth/register")
    wait_for_stability(page)

    # 2. Logic (using POM)
    registration_page = RegistrationPage(page)
    registration_page.navigate_to_registration()
    registration_page.fill_first_name("4072")
    registration_page.fill_last_name("4072")
    registration_page.fill_email("4072@example.com")

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()