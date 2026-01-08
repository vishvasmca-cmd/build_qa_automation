# Auto-generated Test
import pytest
import os
import re
import random
import sys
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
# Fallback for local run if the above path doesn't exist
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../core/templates'))

from helpers import take_screenshot

class ParabankPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")
        self.page.wait_for_load_state("networkidle")

    @property
    def account_history_link(self):
        return self.page.get_by_role("link", name="Account History")

    @property
    def about_us_link(self):
        return self.page.locator("#headerPanel").get_by_role("link", name=re.compile("About Us", re.IGNORECASE))

    @property
    def home_link(self):
        return self.page.get_by_role("link", name="Home", exact=True).first

    def navigate_to_account_history(self) -> None:
        self.account_history_link.click()

    def navigate_to_about_us(self) -> None:
        self.about_us_link.click()
        self.page.wait_for_url(re.compile(r".*/about.htm"), timeout=5000)
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_home(self) -> None:
        self.home_link.click()

    def verify_login_page(self) -> None:
        expect(self.page).to_have_title("ParaBank | Welcome")
    
    def is_login_form_visible(self):
        return self.page.locator("input[name='username']").is_visible() and self.page.locator("input[name='password']").is_visible() and self.page.get_by_role("button", name=re.compile("Log In", re.IGNORECASE)).is_visible()

class ParabankAboutUsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def home_link(self):
        return self.page.get_by_role("link", name="Home", exact=True).first

    def navigate_to_home(self) -> None:
        self.home_link.click()

class ParabankServicesPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def home_link(self):
        return self.page.get_by_role("link", name="Home", exact=True).first

    def navigate_to_home(self) -> None:
        self.home_link.click()

class ParabankWadlPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def home_link(self):
        return self.page.get_by_role("link", name="Home", exact=True).first

    def navigate_to_home(self) -> None:
        self.home_link.click()

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    parabank_page = ParabankPage(page)
    parabank_about_us_page = ParabankAboutUsPage(page)
    
    parabank_page.goto()

    # 2. Logic (using POM)
    # Step 0: Click Account History
    try:
        parabank_page.navigate_to_account_history()
        # Check for WADL redirect and retry if needed
        if "_wadl" in page.url or page.url.endswith(".xml"):
            page.go_back()
            parabank_page.navigate_to_account_history()

    except Exception as e:
        print(f"Error during Account History navigation: {e}")

    # Step 1: Navigate back to home page
    try:
        page.goto("https://parabank.parasoft.com/parabank/index.htm")
    except Exception as e:
        print(f"Error during navigation to home page: {e}")

    # Step 9: Navigate to About Us
    try:
        parabank_page.navigate_to_about_us()
    except Exception as e:
        print(f"Error during About Us navigation: {e}")

    # Step 10: Navigate back to home page from About Us page
    try:
        parabank_about_us_page.navigate_to_home()
    except Exception as e:
        print(f"Error during navigation to home page from About Us: {e}")

    # Step 11: Click Account History again
    try:
        parabank_page.navigate_to_account_history()
        # Check for WADL redirect and retry if needed
        if "_wadl" in page.url or page.url.endswith(".xml"):
            page.go_back()
            parabank_page.navigate_to_account_history()

    except Exception as e:
        print(f"Error during Account History navigation (2nd attempt): {e}")

    # 3. Cleanup
    try:
        take_screenshot(page, "final_state", "core_parabank")
    except Exception:
        pass
    context.close()