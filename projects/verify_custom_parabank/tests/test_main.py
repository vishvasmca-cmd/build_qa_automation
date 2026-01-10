# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
# Dynamic path discovery: Find root of 'inner-event' and append core path
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to project root (e.g., projects/name/tests/ -> inner-event)
# We assume tests are usually in projects/<name>/tests/ or projects/<name>/tests/e2e
root_dir = current_dir
for _ in range(10): # Max depth search
    if os.path.exists(os.path.join(root_dir, 'core')):
        break
    parent = os.path.dirname(root_dir)
    if parent == root_dir: break
    root_dir = parent

sys.path.append(os.path.join(root_dir, 'core', 'lib', 'templates'))
try:
    from helpers import take_screenshot
except ImportError:
    # Fallback for different structures
    sys.path.append(os.path.abspath(os.path.join(current_dir, '../../../../core/lib/templates')))
    from helpers import take_screenshot


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.register_link = self.page.get_by_role("link", name="Register")

    def navigate_to_registration(self):
        self.register_link.click()
        self.page.wait_for_url("**/register.htm*")

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_field = self.page.locator("[name='username']")

    def fill_username(self, username):
        self.username_field.fill(username)

def test_autonomous_flow(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    registration_page = RegistrationPage(page)

    login_page.navigate("https://parabank.parasoft.com/parabank/index.htm")
    login_page.navigate_to_registration()

    registration_page.fill_username("test")
    registration_page.fill_username("John")
    registration_page.fill_username("test")
