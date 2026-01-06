# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
from helpers import wait_for_stability, smart_action, take_screenshot


class OfficeHomePage:
    def __init__(self, page):
        self.page = page

    @property
    def products_button(self):
        return self.page.locator("#c-shellmenu_0")

    @property
    def power_platform_link(self):
        return self.page.get_by_label("Microsoft Power Platform Business")

    def scroll_to_products(self):
        smart_action(self.page, self.products_button, 'scroll', value='Products')
        wait_for_stability(self.page)
        expect(self.products_button).to_be_visible()

    def scroll_to_power_platform(self):
        smart_action(self.page, self.power_platform_link, 'scroll', value='Microsoft Power Platform Business')
        wait_for_stability(self.page)
        expect(self.power_platform_link).to_be_visible()


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://www.office.com/")
    wait_for_stability(page)

    # 2. Logic (using POM)
    office_home_page = OfficeHomePage(page)
    office_home_page.scroll_to_products()
    office_home_page.scroll_to_power_platform()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()