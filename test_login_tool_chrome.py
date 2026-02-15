
import asyncio
from playwright.async_api import async_playwright
from core.lib.webmcp_polyfill import (
    WebMCPPolyfill,
    create_login_tool_polyfill
)

async def test_login():
    print("Testing WebMCP Login Tool in Chrome...")
    webmcp = WebMCPPolyfill()
    webmcp.register_tool(create_login_tool_polyfill())
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            channel="chrome",
            slow_mo=1000
        )
        page = await browser.new_page()
        
        print(f"Launched Chrome: {browser.version}")
        
        print("Navigating to SauceDemo...")
        await page.goto("https://www.saucedemo.com/")
        
        # Inject tool
        await webmcp.inject_tools(page)
        
        print("Executing login tool...")
        result = await webmcp.call_tool(page, "login", {
            "username": "standard_user",
            "password": "secret_sauce"
        })
        
        if result.get("success"):
            print("✅ Login Tool SUCCESS!")
            print(f"   URL: {page.url}")
        else:
            print(f"❌ Login Tool FAILED: {result.get('error')}")
            
        await asyncio.sleep(2)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_login())
