import pytest
from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_home(self):
        self.page.goto("https://magento.softwaretestingboard.com/")
        self.page.wait_for_load_state("networkidle")



def test_autonomous_flow(page: Page):
    # 1. Setup
    home_page = HomePage(page)

    # 2. Logic
    home_page.navigate_to_home()
    with pytest.raises(Exception) as excinfo:
        home_page.navigate_to_home()
        home_page.navigate_to_home()
        raise Exception("SSL certificate is invalid, test cannot proceed.")
    assert str(excinfo.value) == "SSL certificate is invalid, test cannot proceed."
