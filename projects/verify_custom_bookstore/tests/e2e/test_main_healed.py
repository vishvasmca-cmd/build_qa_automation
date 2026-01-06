# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/templates')
from helpers import wait_for_stability, smart_action, take_screenshot


class BookStorePage:
    def __init__(self, page):
        self.page = page

    @property
    def search_box(self):
        return self.page.locator("#searchBox")

    @property
    def login_button(self):
        return self.page.locator("#login")

    @property
    def book_store_link(self):
        return self.page.locator("#item-2")

    def search_book(self, book_name):
        smart_action(self.page, self.search_box, "fill", value=book_name)
        wait_for_stability(self.page)

    def navigate_to_login(self):
        smart_action(self.page, self.login_button, "click")
        wait_for_stability(self.page)

    def navigate_to_book_store(self):
        smart_action(self.page, self.book_store_link, "click")
        wait_for_stability(self.page)

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://demoqa.com/books")
    wait_for_stability(page)

    # 2. Logic (using POM)
    book_store_page = BookStorePage(page)
    book_store_page.search_book("Learning JavaScript Design Patterns")
    
    book_store_page.navigate_to_login()
    
    book_store_page.navigate_to_book_store()
    
    book_store_page.search_book("Git Pocket Guide")
    
    book_store_page.search_book("Learning JavaScript Design Patterns")

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()