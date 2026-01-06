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


class ComputerDatabasePage:
    def __init__(self, page):
        self.page = page

    @property
    def add_computer_button(self):
        return self.page.get_by_role("link", name="Add a new computer")

    def navigate_to_add_computer(self):
        smart_action(self.page, self.add_computer_button, "click")
        wait_for_stability(self.page)


class AddComputerPage:
    def __init__(self, page):
        self.page = page

    @property
    def computer_name_input(self):
        return self.page.get_by_label("Computer name")

    @property
    def create_button(self):
        return self.page.get_by_role("button", name="Create this computer")

    def fill_computer_name(self, name):
        smart_action(self.page, self.computer_name_input, "fill", value=name)
        wait_for_stability(self.page)

    def create_computer(self):
        smart_action(self.page, self.create_button, "click")
        wait_for_stability(self.page)


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://computer-database.gatling.io/computers")
    wait_for_stability(page)

    # 2. Logic (using POM)
    computer_db_page = ComputerDatabasePage(page)
    add_computer_page = AddComputerPage(page)

    computer_db_page.navigate_to_add_computer()
    add_computer_page.fill_computer_name("Test Computer")
    add_computer_page.create_computer()
    
    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()