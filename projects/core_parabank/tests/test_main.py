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


class ParabankPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")
        self.page.wait_for_load_state("domcontentloaded")

    @property
    def about_us_link(self):
        return self.page.locator("#headerPanel").get_by_role("link", name=re.compile("About Us", re.IGNORECASE))

    @property
    def home_link(self):
        return self.page.locator("#headerPanel").get_by_role("link", name=re.compile("Home", re.IGNORECASE))

    def navigate_to_about_us(self):
        self.about_us_link.click()
        self.page.wait_for_url(re.compile(r".*/about.htm"), timeout=5000)
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_home(self):
        self.home_link.click()
        self.page.wait_for_url("https://parabank.parasoft.com/parabank/index.htm", timeout=5000)
        self.page.wait_for_load_state("domcontentloaded")

    def is_login_form_visible(self):
        return self.page.locator("input[name='username']").is_visible() and self.page.locator("input[name='password']").is_visible() and self.page.get_by_role("button", name=re.compile("Log In", re.IGNORECASE)).is_visible()


class ParabankAboutUsPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def home_link(self):
        return self.page.locator("#headerPanel").get_by_role("link", name=re.compile("Home", re.IGNORECASE))

    def navigate_to_home(self):
        self.home_link.click()
        self.page.wait_for_url("https://parabank.parasoft.com/parabank/index.htm", timeout=5000)
        self.page.wait_for_load_state("domcontentloaded")


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    parabank_page = ParabankPage(page)
    about_us_page = ParabankAboutUsPage(page)

    # 2. Logic (using POM)
    parabank_page.goto()
    parabank_page.navigate_to_about_us()
    expect(page).to_have_url(re.compile(r".*/about.htm"))
    about_us_page.navigate_to_home()
    expect(page).to_have_url("https://parabank.parasoft.com/parabank/index.htm")

    # Verify login form is visible
    assert parabank_page.is_login_form_visible(), "Login form is not visible"

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()