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


class InmobiHomePage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://www.inmobi.com/")
        wait_for_stability(self.page)

    @property
    def accept_all_button(self):
        return self.page.get_by_role("button", name="ACCEPT ALL")

    @property
    def learn_more_link(self):
        return self.page.get_by_role("link", name="Learn More")

    def accept_cookies(self):
        smart_action(self.page, self.accept_all_button, "click")
        wait_for_stability(self.page)

    def scroll_down(self):
        smart_action(self.page, self.learn_more_link, "scroll")
        wait_for_stability(self.page)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home_page = InmobiHomePage(page)

    # 2. Logic (using POM)
    home_page.goto()
    home_page.accept_cookies()
    home_page.scroll_down()
    home_page.scroll_down()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()