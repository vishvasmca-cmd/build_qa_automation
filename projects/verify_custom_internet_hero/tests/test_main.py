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
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_field = self.page.locator("#username")
        self.password_field = self.page.locator("#password")
        self.login_button = self.page.get_by_role("button", name=re.compile("Login", re.IGNORECASE))
        self.form_authentication_link = self.page.get_by_role("link", name=re.compile("Form Authentication", re.IGNORECASE))

    def navigate_to_login_page(self):
        self.navigate("https://the-internet.herokuapp.com/")
        self.form_authentication_link.click()
        self.page.wait_for_url("**/login")

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()


class SecurePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)

    login_page.navigate_to_login_page()
    login_page.login("tomsmith", "SuperSecretPassword!")

    page.wait_for_url("**/secure")
    expect(page.locator("#flash")).to_be_visible()
    take_screenshot(page, "login_success", "the-internet")
