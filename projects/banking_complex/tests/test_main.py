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
        self.page.wait_for_load_state("networkidle")

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

from playwright.sync_api import Browser

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    home_page = HomePage(page)
    home_page.navigate("https://parabank.parasoft.com/parabank/index.htm")
    take_screenshot(page, 'home_page', 'parabank')

    # Assert that the title is correct
    expect(page).to_have_title(re.compile("ParaBank", re.IGNORECASE))
