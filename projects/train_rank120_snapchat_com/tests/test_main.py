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


class SnapchatHomePage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://www.snapchat.com/")
        wait_for_stability(self.page)

    @property
    def community_geofilter_terms_link(self):
        return self.page.get_by_role("link", name="Community Geofilter Terms")

    def scroll_to_community_geofilter_terms(self):
        smart_action(self.page, self.community_geofilter_terms_link, "scroll")

    def scroll_to_report_infringement(self):
        report_infringement_link = self.page.get_by_role("link", name="Report Infringement")
        smart_action(self.page, report_infringement_link, "scroll")
        expect(report_infringement_link).to_be_visible()


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    snapchat_home_page = SnapchatHomePage(page)
    snapchat_home_page.goto()

    # 2. Logic (using POM)
    snapchat_home_page.scroll_to_community_geofilter_terms()
    snapchat_home_page.scroll_to_report_infringement()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()