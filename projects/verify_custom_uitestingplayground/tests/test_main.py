# Auto-generated Test
import pytest
import re
from playwright.sync_api import Page, Browser, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")


class UiTestAutomationPlaygroundPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dynamic_id_link = self.page.get_by_role("link", name=re.compile("Dynamic ID", re.IGNORECASE))

    def navigate_to_dynamic_id(self):
        self.dynamic_id_link.click()
        self.page.wait_for_url("**/dynamicid")
        self.page.wait_for_load_state()


class DynamicIdPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_with_dynamic_id = self.page.get_by_role("button", name=re.compile("Button with Dynamic ID", re.IGNORECASE))

    def click_button_with_dynamic_id(self):
        self.button_with_dynamic_id.click()


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    base_url = "http://uitestingplayground.com/"

    # Initialize pages
    base_page = BasePage(page)
    home_page = UiTestAutomationPlaygroundPage(page)
    dynamic_id_page = DynamicIdPage(page)

    # Navigate to the home page
    base_page.navigate(base_url)

    # Navigate to the Dynamic ID page
    home_page.navigate_to_dynamic_id()

    # Click the button with the dynamic ID
    dynamic_id_page.click_button_with_dynamic_id()

    # Assertion to verify the button was clicked
    expect(dynamic_id_page.button_with_dynamic_id).to_be_visible()

    page.close()