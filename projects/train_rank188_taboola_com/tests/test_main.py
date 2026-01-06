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


class TaboolaHomePage:
    def __init__(self, page):
        self.page = page

    @property
    def engagement_button(self):
        return self.page.get_by_role("button", name="Engagement")

    @property
    def performance_marketing_platforms_link(self):
        return self.page.get_by_role("link", name="Performance Marketing Platforms")

    def scroll_to_engagement(self):
        smart_action(self.page, self.engagement_button, "scroll")
        wait_for_stability(self.page)

    def scroll_to_performance_marketing_platforms(self):
        smart_action(self.page, self.performance_marketing_platforms_link, "scroll")
        wait_for_stability(self.page)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://www.taboola.com/")
    wait_for_stability(page)

    # 2. Logic (using POM)
    taboola_home_page = TaboolaHomePage(page)
    taboola_home_page.scroll_to_engagement()
    taboola_home_page.scroll_to_performance_marketing_platforms()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()