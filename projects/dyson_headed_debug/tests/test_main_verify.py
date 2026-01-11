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


from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def close_popup(self):
        try:
            self.page.get_by_text("X").click()
        except Exception:
            pass

from playwright.sync_api import Page


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate(self):
        self.page.goto("https://www.dyson.in/")

    def click_deals_link(self):
        self.page.get_by_role("link", name=re.compile("Deals", re.IGNORECASE)).click()
        self.page.wait_for_url("**/deals")
        self.wait_for_stability()

    def click_vacuum_wet_cleaners_link(self):
        self.page.get_by_role("link", name=re.compile("Vacuum & wet cleaners", re.IGNORECASE)).click()
        self.page.wait_for_url("**/vacuum-cleaners")
        self.wait_for_stability()

    def click_hair_care_link(self):
        self.page.get_by_role("link", name=re.compile("Hair care", re.IGNORECASE)).click()
        self.page.wait_for_url("**/hair-care")
        self.wait_for_stability()

    def click_air_purifier_link(self):
        self.page.get_by_role("link", name=re.compile("Air purifier", re.IGNORECASE)).click()
        self.page.wait_for_url("**/air-treatment")
        self.wait_for_stability()

    def click_headphones_link(self):
        self.page.get_by_role("link", name=re.compile("Headphones", re.IGNORECASE)).click()
        self.page.wait_for_url("**/headphones")
        self.wait_for_stability()

    def click_lighting_link(self):
        self.page.get_by_role("link", name=re.compile("Lighting", re.IGNORECASE)).click()
        self.page.wait_for_url("**/lighting")
        self.wait_for_stability()

    def click_support_link(self):
        self.page.get_by_role("link", name=re.compile("Support", re.IGNORECASE)).click()
        self.page.wait_for_url("**/support")
        self.wait_for_stability()

    def wait_for_stability(self):
        self.page.wait_for_load_state('networkidle')


from playwright.sync_api import sync_playwright, Browser
from pages.home_page import HomePage
from pytest import expect

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    home_page = HomePage(page)
    home_page.navigate()
    home_page.close_popup()
    home_page.click_deals_link()
    expect(page.url).to_contain(re.compile("/deals", re.IGNORECASE))
    home_page.click_vacuum_wet_cleaners_link()
    expect(page.url).to_contain(re.compile("/vacuum-cleaners", re.IGNORECASE))
    home_page.click_hair_care_link()
    expect(page.url).to_contain(re.compile("/hair-care", re.IGNORECASE))
    home_page.click_air_purifier_link()
    expect(page.url).to_contain(re.compile("/air-treatment", re.IGNORECASE))
    home_page.click_headphones_link()
    expect(page.url).to_contain(re.compile("/headphones", re.IGNORECASE))
    home_page.click_lighting_link()
    expect(page.url).to_contain(re.compile("/lighting", re.IGNORECASE))
    home_page.click_support_link()
    expect(page.url).to_contain(re.compile("/support", re.IGNORECASE))
    page.close()
