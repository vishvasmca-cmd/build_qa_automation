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
        password = f'password_{timestamp}'
        email = f'test_{timestamp}@example.com'
        page.context.set_default_timeout(30000) # Match helper timeout
        
        # Generated for verify_custom_demoblaze
        page.goto("https://www.demoblaze.com/")
        wait_for_stability(page)
    
        
        smart_action(page, "page.get_by_role(\"link\", name=\"Sign up\")", "click")
        wait_for_stability(page)
        smart_action(page, "page.locator(\"#sign-username\")", "fill", value=username)
        wait_for_stability(page)
        smart_action(page, "page.locator(\"#sign-password\")", "fill", value=password)
        wait_for_stability(page)
        smart_action(page, "page.get_by_role(\"button\", name=\"Sign up\")", "click")
        wait_for_stability(page)
        #Optional: Add an assertion to check for successful signup
        #expect(page.locator("div#login-username")).to_be_visible()
    
        take_screenshot(page, "final_state", "verify_custom_demoblaze")
        
    finally:
        context.close()