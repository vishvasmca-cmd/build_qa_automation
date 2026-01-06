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


class DzenPage:
    def __init__(self, page):
        self.page = page

    @property
    def login_button(self):
        return self.page.get_by_role("button", name=re.compile("Log in", re.IGNORECASE))

    @property
    def sport_tab(self):
        return self.page.get_by_text("Спорт", exact=True)

    def scroll_to_login(self):
        smart_action(self.page, self.login_button, "scroll")
        wait_for_stability(self.page)

    def scroll_to_sport(self):
        smart_action(self.page, self.sport_tab, "scroll")
        wait_for_stability(self.page)

    def click_sport_tab(self):
        smart_action(self.page, self.sport_tab, "click")
        self.page.wait_for_url("**/sport", timeout=10000)
        wait_for_stability(self.page)


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://dzen.ru/?yredirect=true")
    wait_for_stability(page)

    # 2. Logic (using POM)
    dzen_page = DzenPage(page)
    dzen_page.scroll_to_login()
    dzen_page.scroll_to_sport()
    dzen_page.click_sport_tab()
