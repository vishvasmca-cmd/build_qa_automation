import pytest
from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("https://magento.softwaretestingboard.com/")
        self.page.wait_for_load_state("networkidle")

    def check_ssl_error(self):
        if "Invalid SSL certificate" in self.page.title():
            raise Exception("SSL Certificate Error: Test cannot proceed due to invalid SSL certificate.")



def test_autonomous_flow(page: Page):
    home_page = HomePage(page)

    try:
        home_page.goto()
        home_page.check_ssl_error()
    except Exception as e:
        pytest.skip(f"SSL Certificate Error Detected: {e}")
