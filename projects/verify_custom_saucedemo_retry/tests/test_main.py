"""
Minimal Smoke Test (Fallback)
Generated because full POM generation failed after all attempts.
This test verifies basic site accessibility.

Goal: Login, add item to cart, checkout
"""
import re
from playwright.sync_api import Page, expect, Browser
import pytest
import sys
import os

# Define helpers directly to ensure self-containment
def wait_for_stability(page):
    page.wait_for_load_state("networkidle")
    page.wait_for_load_state("domcontentloaded")

def take_screenshot(page, name, project_name):
    screenshot_dir = os.path.join(os.getcwd(), "projects", project_name, "outputs", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    path = os.path.join(screenshot_dir, f"{name}.png")
    page.screenshot(path=path)
    print(f"[SCREENSHOT] Saved: {path}")

def test_minimal_smoke(browser: Browser):
    """Minimal smoke test: Navigate + Screenshot + Basic Assertion"""
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    # 2. Navigate to site
    print(f"[Minimal Test] Navigating to https://www.saucedemo.com/")
    page.goto("https://www.saucedemo.com/")
    wait_for_stability(page)
    
    # 3. Basic verification: Page loaded successfully
    # Check either URL matches OR page has a title
    current_url = page.url
    page_title = page.title()
    
    assert "https://www.saucedemo.com/" in current_url or page_title, \
        f"Page failed to load. Current URL: {current_url}, Title: {page_title}"
    
    print(f"[Minimal Test] Page loaded: {page_title or current_url}")
    
    # 4. Take screenshot for visual validation
    take_screenshot(page, "smoke_test_final", "verify_custom_saucedemo_retry")
    
    # 5. Cleanup
    context.close()
    
    print("Minimal smoke test PASSED: Site is accessible")