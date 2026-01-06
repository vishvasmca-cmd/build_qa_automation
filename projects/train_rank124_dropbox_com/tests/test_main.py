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


class DropboxHomePage:
    def __init__(self, page):
        self.page = page

    def scroll_feature_highlight_path(self):
        feature_highlight_scroll_path = self.page.locator("xpath=//*[@id=\"dwg_feature_highlight_plank-9c48824da7\"]/div[1]/div[1]/div[1]/div[2]/a[1]/div[1]/span[2]/span[1]/svg[1]/path[1]")
        smart_action(self.page, feature_highlight_scroll_path, "scroll")
        wait_for_stability(self.page)

    def scroll_feature_highlight_svg(self):
        feature_highlight_scroll_svg = self.page.locator("xpath=//*[@id=\"dwg_feature_highlight_plank-9c48824da7\"]/div[1]/div[1]/div[1]/div[2]/a[1]/div[1]/span[2]/span[1]/svg[1]")
        smart_action(self.page, feature_highlight_scroll_svg, "scroll")
        wait_for_stability(self.page)


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://www.dropbox.com/")
    wait_for_stability(page)

    # 2. Logic (using POM)
    dropbox_home_page = DropboxHomePage(page)
    dropbox_home_page.scroll_feature_highlight_path()
    dropbox_home_page.scroll_feature_highlight_svg()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()