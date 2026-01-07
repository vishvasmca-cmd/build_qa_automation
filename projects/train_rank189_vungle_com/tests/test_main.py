# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
from helpers import take_screenshot


class HomePage:
    def __init__(self, page):
        self.page = page

    @property
    def log_in_button(self):
        return self.page.get_by_role("button", name="Log In")

    @property
    def lang_selector(self):
        return self.page.locator(".txlive-langselector-marker")

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://liftoff.ai/")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    home_page = HomePage(page)

    # Step 0: Verify and click Log In button
    log_in_button = home_page.log_in_button
    expect(log_in_button).to_be_visible()
    log_in_button.click()
    page.wait_for_url('**/login', timeout=60000)

    # Step 1: Scroll the page
    home_page.lang_selector.scroll_into_view_if_needed()

    # Step 2: Verify Log In button is still present
    expect(home_page.log_in_button).to_be_visible()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()