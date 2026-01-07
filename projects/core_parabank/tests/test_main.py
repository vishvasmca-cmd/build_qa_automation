# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/templates')
from helpers import take_screenshot


class ParabankPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")
        self.page.wait_for_load_state("networkidle")

    @property
    def about_us_link(self):
        return self.page.locator("#headerPanel").get_by_role("link", name="About Us")

    @property
    def account_history_link(self):
        return self.page.get_by_role("link", name="Account History")

    def navigate_to_about_us(self):
        self.about_us_link.click()

    def navigate_to_account_history(self):
        self.account_history_link.click()

class ParabankAboutUsPage:
    def __init__(self, page):
        self.page = page

    @property
    def home_link(self):
        return self.page.get_by_role("link", name="Home")

    def navigate_to_home(self):
        self.home_link.first.click()

class ParabankWadlPage:
    def __init__(self, page):
        self.page = page

    def navigate_to_home(self):
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")
        self.page.wait_for_load_state("networkidle")

class ParabankServicesBankXmlDefinitionPage:
    def __init__(self, page):
        self.page = page

    def navigate_to_home(self):
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")
        self.page.wait_for_load_state("networkidle")

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # 2. Logic (using POM)
    parabank_page = ParabankPage(page)
    parabank_about_us_page = ParabankAboutUsPage(page)
    parabank_wadl_page = ParabankWadlPage(page)
    parabank_services_bank_xml_definition_page = ParabankServicesBankXmlDefinitionPage(page)

    parabank_page.goto()
    parabank_page.navigate_to_about_us()

    parabank_about_us_page.navigate_to_home()
    parabank_page.navigate_to_about_us()

    parabank_about_us_page.navigate_to_home()
    parabank_page.navigate_to_account_history()

    parabank_wadl_page.navigate_to_home()

    parabank_services_bank_xml_definition_page.navigate_to_home()

    parabank_services_bank_xml_definition_page.navigate_to_home()

    parabank_services_bank_xml_definition_page.navigate_to_home()

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()