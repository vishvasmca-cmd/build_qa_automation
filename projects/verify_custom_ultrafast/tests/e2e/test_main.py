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


def test_autonomous_flow(browser: Browser):
    """Auto-generated test from trace"""
    # 1. Config: Avoiding Bot Detection
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="en-US"
    )
    page = context.new_page()
    
    try:
        timestamp = random.randint(1000, 9999)
        username = f'user_{timestamp}'
        email = f'test_{timestamp}@example.com'
        page.context.set_default_timeout(30000) # Match helper timeout
        
        # Generated for verify_custom_ultrafast
        page.goto("https://demo.applitools.com/")
        wait_for_stability(page)

        # Step 0: Fill username field
        smart_action(page, "#username", "fill", value="test")
        wait_for_stability(page)
        
        # Step 1: Fill password field
        smart_action(page, "#password", "fill", value="password")
        wait_for_stability(page)
        
        # Step 2: Click the login button
        smart_action(page, "#log-in", "click")
        wait_for_stability(page)

        # Step 3: Verify successful login (check for logout button)
        expect(page.locator("#logout")).to_be_visible()

        # Step 4: Take screenshot of successful login
        take_screenshot(page, "login_success")

        take_screenshot(page, "final_state", "verify_custom_ultrafast")

    finally:
        context.close()
