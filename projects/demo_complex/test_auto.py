import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/templates')
from helpers import wait_for_stability, smart_action, take_screenshot


class ContactUsPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("https://automationexercise.com/contact_us")

    def fill_contact_form(self, name, email, subject):
        self.page.locator("[name='name']").fill(name)
        self.page.locator("[name='email']").fill(email)
        self.page.locator("[name='subject']").fill(subject)


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("https://automationexercise.com/")

    def navigate_to_contact_us(self):
        self.page.get_by_role("link", name="Contact us").click()
        self.page.wait_for_url("https://automationexercise.com/contact_us")


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home_page = HomePage(page)
    contact_us_page = ContactUsPage(page)

    # 2. Logic (using POM)
    home_page.goto()
    home_page.navigate_to_contact_us()
    contact_us_page.fill_contact_form("Test User", "test@example.com", "Support")

    # Assertion: Check if the URL is correct after navigation
    expect(page).to_have_url("https://automationexercise.com/contact_us")

    # 3. Cleanup
    take_screenshot(page, "final_state", "inner-event")
    context.close()
