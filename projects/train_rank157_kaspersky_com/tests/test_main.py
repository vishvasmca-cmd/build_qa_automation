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
    def __init__(self, page: Page):
        self.page = page

    def accept_and_close(self):
        self.page.get_by_role("button", name=re.compile("ACCEPT AND CLOSE", re.IGNORECASE)).click()
        self.page.locator("#onetrust-pc-sdk").wait_for(state="detached", timeout=10000)


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://kaspersky.com")
    page.wait_for_load_state("networkidle")
    
    # 2. Logic (using POM)
    home_page = HomePage(page)
    home_page.accept_and_close()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()