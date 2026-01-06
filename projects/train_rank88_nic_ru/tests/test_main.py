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


class NicRuHomePage:
    def __init__(self, page):
        self.page = page

    @property
    def individual_service_text(self):
        return self.page.get_by_text(re.compile("Индивидуальное обслуживание для вашей компании", re.IGNORECASE), exact=False)

    @property
    def scrollable_area(self):
        return self.page.locator("[data-agent-id='0']")

    def scroll_down(self):
        smart_action(self.page, self.scrollable_area, 'scroll', value='scroll down')
        wait_for_stability(self.page)

    def scroll_to_individual_service(self):
        smart_action(self.page, self.individual_service_text, 'scroll')
        wait_for_stability(self.page)

    def handle_modal(self):
        try:
            close_button = self.page.get_by_role("button", name=re.compile("Закрыть", re.IGNORECASE))
            if close_button.is_visible(timeout=5000):
                smart_action(self.page, close_button, 'click')
                wait_for_stability(self.page)
        except Exception:
            pass


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://nic.ru")
    wait_for_stability(page)

    # 2. Logic (using POM)
    nic_ru_home_page = NicRuHomePage(page)
    nic_ru_home_page.handle_modal()
    wait_for_stability(page)
    nic_ru_home_page.scroll_down()
    nic_ru_home_page.scroll_to_individual_service()

    # 3. Cleanup
    take_screenshot(page, 'final_state', 'test-results')
    context.close()