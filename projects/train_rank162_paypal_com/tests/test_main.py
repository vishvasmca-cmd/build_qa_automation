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


class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        self.page.goto("https://www.paypal.com/us/home")
        wait_for_stability(self.page)

    @property
    def terms_link(self):
        return self.page.get_by_text("Terms")

    def scroll_to_terms(self) -> None:
        smart_action(self.page, self.terms_link, "scroll")
        wait_for_stability(self.page)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home_page = HomePage(page)

    # 2. Logic (using POM)
    home_page.goto()
    home_page.scroll_to_terms()
    home_page.scroll_to_terms()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()