# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
# Dynamic path discovery: Find root of 'inner-event' and append core path
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to project root (e.g., projects/name/tests/ -> inner-event)
# We assume tests are usually in projects/<name>/tests/ or projects/<name>/tests/e2e
root_dir = current_dir
for _ in range(10):  # Max depth search
    if os.path.exists(os.path.join(root_dir, 'core')):
        break
    parent = os.path.dirname(root_dir)
    if parent == root_dir: break
    root_dir = parent

sys.path.append(os.path.join(root_dir, 'core', 'lib', 'templates'))
try:
    from helpers import take_screenshot
except ImportError:
    # Fallback for different structures
    sys.path.append(os.path.abspath(os.path.join(current_dir, '../../../../core/lib/templates')))
    from helpers import take_screenshot


class BasePage:
    def __init__(self, page: Page):
        self.page = page


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    def navigate(self):
        self.page.goto("https://www.dyson.in/")

    def click_menu_item(self, item_name: str):
        self.page.get_by_role("link", name=re.compile(item_name, re.IGNORECASE)).click()
        self.page.wait_for_url(re.compile(item_name.lower().replace(' ', '-')), timeout=60000)
        self.page.wait_for_load_state()


@pytest.mark.parametrize("menu_item", ["Deals", "Vacuum & wet cleaners", "Hair care", "Air purifier", "Headphones", "Lighting", "Support"])
def test_autonomous_flow(browser: Browser, menu_item: str):
    page = browser.new_page()
    home_page = HomePage(page)
    home_page.navigate()

    home_page.click_menu_item(menu_item)
    expect(page).to_have_url(re.compile(menu_item.lower().replace(' ', '-')), timeout=60000)

    page.close()