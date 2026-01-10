# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/lib/templates')
from helpers import take_screenshot


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click_demo_link(self):
        self.page.get_by_role("link", name="Demo").first.click()

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_hotels_link(self):
        self.page.get_by_role("link", name="Hotels").click()

    def enter_destination(self, destination):
        self.page.locator("[aria-label='Going to']").fill(destination)

    def select_destination(self, destination):
        self.page.locator("#select2-drop .select2-result-label").first.click()

    def click_search_button(self):
        self.page.get_by_role("button", name="Search").click()

def test_autonomous_flow(browser):
    page = browser.new_page()
    base_page = BasePage(page)
    home_page = HomePage(page)

    base_page.navigate("https://phptravels.com/demo/")
    base_page.click_demo_link()
    page.wait_for_load_state("networkidle")

    home_page.click_hotels_link()
    home_page.enter_destination("Dubai")
    home_page.select_destination("Dubai")
    home_page.click_search_button()
    page.wait_for_load_state("networkidle")

    take_screenshot(page, "hotel_search_results", "verify_custom_phptravels")