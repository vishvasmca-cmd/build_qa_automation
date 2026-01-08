"""
Minimal Template Generator (Fallback System)
Generates a basic smoke test when full POM generation fails.
This ensures 100% of sites get SOME automated test coverage.
"""
import os
import json

def generate_minimal_smoke_test(config, output_path):
    """
    Generates a minimal working smoke test when full generation fails.
    
    Args:
        config: Project configuration dictionary
        output_path: Path where test file should be written
    
    Returns:
        bool: True if successful, False otherwise
    """
    target_url = config.get("target_url", "https://example.com")
    project_name = config.get("project_name", "unknown_project")
    workflow_goal = config.get("workflow_description") or config.get("goal", "Explore the site")
    
    # Generate minimal but valid test
    template = f'''"""
Minimal Smoke Test (Fallback)
Generated because full POM generation failed after all attempts.
This test verifies basic site accessibility.

Goal: {workflow_goal}
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
    context = browser.new_context(viewport={{"width": 1920, "height": 1080}})
    page = context.new_page()
    
    # 2. Navigate to site
    print(f"[Minimal Test] Navigating to {target_url}")
    page.goto("{target_url}")
    wait_for_stability(page)
    
    # 3. Basic verification: Page loaded successfully
    # Check either URL matches OR page has a title
    current_url = page.url
    page_title = page.title()
    
    assert "{target_url}" in current_url or page_title, \\
        f"Page failed to load. Current URL: {{current_url}}, Title: {{page_title}}"
    
    print(f"[Minimal Test] ✅ Page loaded: {{page_title or current_url}}")
    
    # 4. Take screenshot for visual validation
    take_screenshot(page, "smoke_test_final", "{project_name}")
    
    # 5. Cleanup
    context.close()
    
    print("✅ Minimal smoke test PASSED: Site is accessible")
'''
    
    # Write to output
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(template)
    
    print(f"📝 Minimal smoke test generated: {output_path}")
    print(f"   Goal captured: {workflow_goal[:100]}...")
    return True

if __name__ == "__main__":
    # Test the generator
    test_config = {
        "target_url": "https://example.com",
        "project_name": "test_minimal",
        "workflow_description": "Test navigation and basic page load"
    }
    generate_minimal_smoke_test(test_config, "test_minimal_output.py")
