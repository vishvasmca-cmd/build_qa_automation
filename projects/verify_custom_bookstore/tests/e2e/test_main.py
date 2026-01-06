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

    def search_book(self, book_name):
        smart_action(self.page, self.search_box, "fill", book_name)
        wait_for_stability(self.page)


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://demoqa.com/books")
    wait_for_stability(page)

    # 2. Logic (using POM)
    book_store_page = BookStorePage(page)
    book_store_page.search_book("The lord of the rings")
    book_store_page.search_book("Eloquent JavaScript")
    book_store_page.search_book("Git Pocket Guide")

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()