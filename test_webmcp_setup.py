"""
WebMCP Configuration Test - Verify Chrome 145+ Setup

This script tests:
1. System Chrome availability
2. WebMCP (navigator.modelContext) API availability
3. Tool registration and execution

Run this to verify your Chrome upgrade before using WebMCP in tests.
"""

import asyncio
from playwright.async_api import async_playwright


async def test_webmcp_setup():
    print("=" * 60)
    print("WebMCP Chrome 145+ Configuration Test")
    print("=" * 60)
    
    async with async_playwright() as p:
        try:
            # Try to launch Chrome
            print("\n[1/4] Launching system Chrome...")
            browser = await p.chromium.launch(
                headless=False,  # Show browser for visual confirmation
                channel='chrome'
            )
            print("  ✅ System Chrome launched successfully")
            
            # Get browser version
            version = browser.version
            print(f"  ℹ️  Chrome version: {version}")
            
            # Check if version is 145+
            major_version = int(version.split('.')[0])
            if major_version >= 145:
                print(f"  ✅ Chrome {major_version} supports WebMCP")
            else:
                print(f"  ⚠️  Chrome {major_version} may not support WebMCP (need 145+)")
                print("     Consider using channel='chrome-canary' or update Chrome")
            
            # Create page
            page = await browser.new_page()
            print("\n[2/4] Checking WebMCP API availability...")
            
            # Check if navigator.modelContext exists
            webmcp_available = await page.evaluate("""
                () => typeof navigator.modelContext !== 'undefined'
            """)
            
            if webmcp_available:
                print("  ✅ navigator.modelContext API is available!")
            else:
                print("  ❌ navigator.modelContext API NOT available")
                print("     Solutions:")
                print("     1. Use Chrome Canary: channel='chrome-canary'")
                print("     2. Enable WebMCP flag in chrome://flags")
                print("     3. Fallback: Use webmcp_polyfill.py instead")
            
            # Test tool registration (if WebMCP available)
            if webmcp_available:
                print("\n[3/4] Testing tool registration...")
                
                await page.add_init_script("""
                    navigator.modelContext.registerTool({
                        name: 'test_tool',
                        description: 'Simple test tool',
                        input_schema: {
                            type: 'object',
                            properties: {
                                message: {type: 'string'}
                            }
                        },
                        execute: async (params) => {
                            return {
                                success: true,
                                echo: params.message,
                                timestamp: Date.now()
                            };
                        }
                    });
                    console.log('[WebMCP] Test tool registered');
                """)
                
                # Navigate to a page to trigger init script
                await page.goto("about:blank")
                
                print("  ✅ Tool registered successfully")
                
                # Test tool execution
                print("\n[4/4] Testing tool execution...")
                result = await page.evaluate("""
                    async () => {
                        return await navigator.modelContext.tools.test_tool.execute({
                            message: 'Hello from WebMCP!'
                        });
                    }
                """)
                
                if result.get('success'):
                    print(f"  ✅ Tool executed successfully!")
                    print(f"     Result: {result}")
                else:
                    print(f"  ❌ Tool execution failed: {result}")
            else:
                print("\n[3/4] Skipping tool registration (WebMCP not available)")
                print("[4/4] Skipping tool execution (WebMCP not available)")
            
            await browser.close()
            
            print("\n" + "=" * 60)
            if webmcp_available:
                print("✅ SUCCESS: WebMCP is fully operational!")
                print("   You can use webmcp_wrapper.py with native support")
            else:
                print("⚠️  WebMCP NOT available on this Chrome version")
                print("   Options:")
                print("   1. Update to Chrome 145+ or use Chrome Canary")
                print("   2. Use webmcp_polyfill.py (no browser upgrade needed)")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print("\nTroubleshooting:")
            print("1. Ensure Google Chrome is installed on your system")
            print("2. Try channel='chrome-canary' instead of 'chrome'")
            print("3. Fallback: Use bundled Chromium (remove channel parameter)")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_webmcp_setup())
