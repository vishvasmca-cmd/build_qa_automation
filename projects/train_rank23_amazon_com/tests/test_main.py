# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
from helpers import take_screenshot, wait_for_stability


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("https://www.amazon.com/")
        wait_for_stability(self.page)

    def scroll_and_find_element(self, locator):
        locator.scroll_into_view_if_needed()

    def count_buttons_and_links(self):
        buttons = self.page.locator('button').count()
        links = self.page.locator('a').count()
        return buttons, links


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home_page = HomePage(page)

    # 2. Logic (using POM)
    home_page.goto()

    # Step 0: Scroll and find 'Continue shopping' button
    continue_shopping_button = page.get_by_role("button", name="Continue shopping")
    home_page.scroll_and_find_element(continue_shopping_button)
    expect(continue_shopping_button).to_be_visible()

    # Step 1: Scroll and find 'Privacy Policy' link
    privacy_policy_link = page.get_by_role("link", name="Privacy Policy")
    home_page.scroll_and_find_element(privacy_policy_link)
    expect(privacy_policy_link).to_be_visible()

    # Count buttons and links on the page
    buttons, links = home_page.count_buttons_and_links()
    print(f"Number of buttons: {buttons}")
    print(f"Number of links: {links}")

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()