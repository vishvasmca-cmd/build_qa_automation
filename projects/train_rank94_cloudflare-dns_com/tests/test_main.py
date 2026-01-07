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


class CloudflareDNSPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://one.one.one.one/dns/")
        wait_for_stability(self.page)

    @property
    def iphone_button(self):
        return self.page.get_by_role("button", name="iPhone")

    @property
    def dns_link(self):
        return self.page.get_by_role("link", name="DNS")

    @property
    def share_button(self):
        return self.page.locator(".button.share-button")

    def scroll_to_iphone_button(self):
        smart_action(self.page, self.iphone_button, "scroll")
        wait_for_stability(self.page)

    def scroll_to_dns_link(self):
        smart_action(self.page, self.dns_link, "scroll")
        wait_for_stability(self.page)

    def scroll_to_share_button(self):
        smart_action(self.page, self.share_button, "scroll", value="bottom")
        wait_for_stability(self.page)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    cloudflare_dns_page = CloudflareDNSPage(page)
    cloudflare_dns_page.goto()

    # 2. Logic (using POM)
    cloudflare_dns_page.scroll_to_iphone_button()
    cloudflare_dns_page.scroll_to_dns_link()
    cloudflare_dns_page.scroll_to_share_button()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()