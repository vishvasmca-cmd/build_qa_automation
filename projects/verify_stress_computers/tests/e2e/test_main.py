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
    def add_computer_button(self):
        return self.page.get_by_role("link", name="Add a new computer")

    def navigate_to_add_computer(self):
        smart_action(self.page, self.add_computer_button, "click")
        wait_for_stability(self.page)

class NewComputerPage:
    def __init__(self, page):
        self.page = page

    @property
    def computer_name_input(self):
        return self.page.get_by_label("Computer name")

    @property
    def create_computer_button(self):
        return self.page.get_by_role("button", name="Create this computer")

    def create_computer(self, computer_name):
        smart_action(self.page, self.computer_name_input, "fill", value=computer_name)
        smart_action(self.page, self.create_computer_button, "click")
        wait_for_stability(self.page)

from playwright.sync_api import Browser

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://computer-database.gatling.io/computers")
    wait_for_stability(page)

    # 2. Logic (using POM)
    home_page = HomePage(page)
    home_page.navigate_to_add_computer()

    new_computer_page = NewComputerPage(page)
    new_computer_page.create_computer("Test Computer")

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()