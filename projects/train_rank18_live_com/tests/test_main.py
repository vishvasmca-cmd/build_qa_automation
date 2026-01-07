import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect


class MicrosoftOutlookEmailAndCalendarSoftwarePage:
    def __init__(self, page):
        self.page = page






def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://www.microsoft.com/en-us/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook?deeplink=%2Fmail%2F0%2F&sdf=0")
    page.wait_for_load_state("networkidle")
    
    # 2. Logic (using POM)
    microsoft_outlook_page = MicrosoftOutlookEmailAndCalendarSoftwarePage(page)

    products_button = page.get_by_role("button", name=re.compile("Products", re.IGNORECASE))
    expect(products_button).to_be_visible()

    outlook_account_button = page.get_by_role("button", name=re.compile("I don’t have an Outlook.com account", re.IGNORECASE))
    expect(outlook_account_button).to_be_visible()

    # 3. Cleanup
    context.close()