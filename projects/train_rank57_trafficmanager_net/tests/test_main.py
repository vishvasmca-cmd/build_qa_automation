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


class GoogleHomePage:
    def __init__(self, page):
        self.page = page

    @property
    def sign_in_button(self):
        return self.page.get_by_role("button", name=re.compile("Sign in", re.IGNORECASE))

    @property
    def store_link(self):
        return self.page.get_by_role("link", name=re.compile("Store", re.IGNORECASE))

    def click_sign_in(self):
        smart_action(self.page, self.sign_in_button, "click")
        self.page.wait_for_url(re.compile(".*accounts.google.com.*", re.IGNORECASE))
        wait_for_stability(self.page)
        expect(self.page).to_have_url(re.compile(".*accounts.google.com.*", re.IGNORECASE))

    def click_store(self):
        smart_action(self.page, self.store_link, "click")
        self.page.wait_for_url(re.compile(".*store.google.com.*", re.IGNORECASE))
        wait_for_stability(self.page)
        expect(self.page).to_have_url(re.compile(".*store.google.com.*", re.IGNORECASE))


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://www.google.com")
    wait_for_stability(page)

    # 2. Logic (using POM)
    google_home_page = GoogleHomePage(page)
    # The sign-in button might not be visible initially, so scroll to it
    # smart_action(page, page.locator('body'), 'scroll', value='0') # Removed unnecessary scroll
    google_home_page.click_sign_in()
    google_home_page.click_store()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()