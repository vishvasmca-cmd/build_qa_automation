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
        self.page.goto(url, timeout=60000)
        self.page.wait_for_load_state("networkidle")

    def click_demo_link(self):
        self.page.get_by_role("link", name="Demo").click()

    def click_hotels_link(self):
        self.page.get_by_role("link", name="Hotels").first.click()


class HomePage:
    def __init__(self, page):
        self.page = page

    def search_destination(self, destination):
        self.page.locator("[aria-label='Search destination']").fill(destination)
        self.page.get_by_text(destination).first.click()


def test_autonomous_flow(browser):
    page = browser.new_page()
    base_page = BasePage(page)
    home_page = HomePage(page)

    base_page.navigate("https://phptravels.com/demo/")
    base_page.click_demo_link()
    base_page.navigate("https://phptravels.com/")
    base_page.click_hotels_link()
    home_page.search_destination("Dubai")
