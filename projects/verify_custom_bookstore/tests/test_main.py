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

    def take_screenshot(self, name, project_name):
        take_screenshot(self.page, name, project_name)

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/login"

    def enter_username(self, username):
        self.page.locator("#userName").fill(username)

    def enter_password(self, password):
        self.page.locator("#password").fill(password)

    def click_login_button(self):
        self.page.locator("#login").click()

class ToolsqaBookStorePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/books"

    def navigate_to_bookstore(self):
        self.page.locator("#item-2").filter(has_text="Book Store").click()

    def search_book(self, book_title):
        self.page.locator("#searchBox").fill(book_title)

    def click_book(self, book_title):
        self.page.get_by_role("link", name=book_title).click()

def test_autonomous_flow(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    bookstore_page = ToolsqaBookStorePage(page)

    login_page.navigate(login_page.url)
    login_page.enter_username("testuser")
    login_page.enter_password("invalid")
    login_page.click_login_button()

    bookstore_page.navigate_to_bookstore()
    bookstore_page.search_book("Git Pocket Guide")
    bookstore_page.click_book("Git Pocket Guide")
