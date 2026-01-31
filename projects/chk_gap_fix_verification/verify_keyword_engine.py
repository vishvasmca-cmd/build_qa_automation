import asyncio
from playwright.async_api import async_playwright
import sys
import os

# Add project root to path
sys.path.insert(0, os.getcwd())

from core.lib.keywords import KeywordEngine

async def test_dropdown_handling():
    print("Starting KeywordEngine Dropdown Verification...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Test Case 1: the-internet.herokuapp.com
        print("\nTest 1: the-internet.herokuapp.com/dropdown")
        await page.goto("https://the-internet.herokuapp.com/dropdown")
        
        # Try to click on the OPTION directly (which is normally invisible)
        # using KeywordEngine.click, which should auto-detect and use select_option
        try:
            # Option 2
            await KeywordEngine.click(page, "#dropdown option[value='2']")
            print("✅ Clicked option[value='2'] execution completed")
            
            # Verify selection
            val = await page.input_value("#dropdown")
            if val == "2":
                print("✅ Verification Passed: Option 2 selected")
            else:
                print(f"❌ Verification Failed: Actual value {val}")
        except Exception as e:
            print(f"❌ Exception during click: {e}")

        # Test Case 2: testpages.herokuapp.com (Alternative site)
        print("\nTest 2: testpages.herokuapp.com")
        await page.goto("https://testpages.herokuapp.com/styled/basic-html-form-test.html")
        
        try:
            # Dropdown Item 2 (value='dd2')
            await KeywordEngine.click(page, "select[name='dropdown'] option[value='dd2']")
            print("✅ Clicked option[value='dd2'] execution completed")
            
            val = await page.input_value("select[name='dropdown']")
            if val == "dd2":
                print("✅ Verification Passed: dd2 selected")
            else:
                print(f"❌ Verification Failed: Actual value {val}")
        except Exception as e:
            print(f"❌ Exception during click: {e}")

        await browser.close()
    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(test_dropdown_handling())
