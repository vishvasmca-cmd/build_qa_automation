
import os
import sys
import json
from core.reviewer import CodeReviewer

def verify():
    print("🚀 Verifying Reviewer Enforcement of New Locator Strategy...")
    reviewer = CodeReviewer()
    
    # Mock bad code using fragile locators
    bad_code = """
import re
from playwright.sync_api import Page, expect

def test_bad_locators(page: Page):
    page.goto("https://magento.softwaretestingboard.com/")
    # BRITTLE CSS & POSITIONAL SELECTORS (Should be rejected/fixed)
    page.locator("div.container > section > div > button.btn-primary").nth(0).click()
    page.wait_for_timeout(2000)
    page.locator("xpath=//button[text()='Submit']").click()
"""
    
    # Save to a temp file
    temp_path = "projects/bad_locator_test.py"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "w") as f:
        f.write(bad_code)
    
    print("🕵️  Invoking Reviewer...")
    # review_and_fix modifies the file if status is FIXED
    result = reviewer.review_and_fix(temp_path)
    
    if result:
        with open(temp_path, "r") as f:
            fixed_code = f.read()
        
        print("\n✨ Reviewer Summary:")
        # We can't easily see the internal JSON but we can see the fixed code
        print("-" * 40)
        print(fixed_code)
        print("-" * 40)
        
        # Check if brittle patterns were removed or if it mentions priority in logs
        if "get_by_role" in fixed_code or "smart_action" in fixed_code:
            print("✅ SUCCESS: Reviewer converted brittle locators to robust ones!")
        else:
            print("⚠️ NOTE: Reviewer kept code as is (check if it was already deemed 'good enough' or if it failed to fix).")
    else:
        print("❌ Reviewer failed to process.")

if __name__ == "__main__":
    verify()
