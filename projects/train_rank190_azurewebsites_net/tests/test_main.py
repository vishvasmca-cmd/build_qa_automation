import pytest
from playwright.sync_api import Page, Browser, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_example(self):
        self.page.goto("https://www.example.com")
        self.page.wait_for_load_state("networkidle")

    def assert_title(self, title: str):
        expect(self.page).to_have_title(title)



def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home_page = HomePage(page)

    # 2. Logic (using POM)
    home_page.navigate_to_example()

    # 3. Assertion
    home_page.assert_title("Example Domain")

    # 4. Cleanup
    context.close()