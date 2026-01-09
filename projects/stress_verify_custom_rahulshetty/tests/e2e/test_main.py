# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/lib/templates')
from helpers import take_screenshot


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name, project_name):
        take_screenshot(self.page, name, project_name)

class RahulShettyAcademyPracticePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.autocomplete_locator = "#autocomplete"

    def fill_country(self, country_name):
        self.page.locator(self.autocomplete_locator).fill(country_name)
        self.page.locator(".ui-menu-item div").filter(has_text=country_name).first.click()

    def get_alert_text(self):
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.page.locator("#name").fill("Test Name")
        self.page.locator("#alertbtn").click()
        return self.page.locator("#name").evaluate("node => node.value")

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    practice_page = RahulShettyAcademyPracticePage(page)
    practice_page.navigate("https://rahulshettyacademy.com/AutomationPractice/")
    practice_page.fill_country("India")

    # TODO: Implement alert handling and verification
    # alert_text = practice_page.get_alert_text()
    # expect(alert_text).to_contain("Test Name")
