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


class UiTestAutomationPlaygroundPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "http://uitestingplayground.com/"

    def navigate_to_dynamic_id(self):
        self.page.get_by_role("link", name="Dynamic ID").click()


class DynamicIdPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_dynamic_id_button(self):
        self.page.get_by_role("button", name="Button with Dynamic ID").click()


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    base_page = BasePage(page)
    ui_playground_page = UiTestAutomationPlaygroundPage(page)
    dynamic_id_page = DynamicIdPage(page)

    ui_playground_page.navigate(ui_playground_page.url)
    ui_playground_page.navigate_to_dynamic_id()
    dynamic_id_page.click_dynamic_id_button()
    expect(page.get_by_role("button", name="Button with Dynamic ID")).to_be_visible()
