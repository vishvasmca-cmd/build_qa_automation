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
        
        # Generated for verify_custom_internet_hero
        page.goto("https://the-internet.herokuapp.com/")
        wait_for_stability(page)

        # Step 0: Navigate to the Form Authentication page
        smart_action(page, 'page.get_by_role("link", name=re.compile("Form Authentication", re.IGNORECASE))', "click")
        page.wait_for_url("https://the-internet.herokuapp.com/login")
        wait_for_stability(page)

        # Step 1: Fill in the username field
        smart_action(page, "#username", "fill", value="tomsmith")
        wait_for_stability(page)

        # Step 2: Fill in the password field
        smart_action(page, "#password", "fill", value="SuperSecretPassword!")
        wait_for_stability(page)


        take_screenshot(page, "final_state", "verify_custom_internet_hero")
        
    finally:
        context.close()