
import asyncio
import json
import os
from playwright.async_api import async_playwright

EXTENSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET_URL = "https://www.saucedemo.com"
TEST_GOAL = "Login as standard_user, add backpack & bike light to cart, and checkout."

async def run():
    print(f"Loading extension from: {EXTENSION_PATH}")
    async with async_playwright() as p:
        # Launch Chrome with the extension loaded
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./tmp/chrome-profile",
            headless=False,
            args=[
                f"--disable-extensions-except={EXTENSION_PATH}",
                f"--load-extension={EXTENSION_PATH}",
                "--enable-logging=stderr", 
                "--v=1" # detailed logging
            ],
            viewport={"width": 1280, "height": 720}
        )

        page = await context.new_page()
        
        # Listen to console messages from both page and service worker
        def handle_console(msg):
            print(f"[CONSOLE] {msg.type}: {msg.text}")
        
        page.on("console", handle_console)
        
        # Listen for service worker console (if available)
        def handle_service_worker_console(msg):
            print(f"[SW-CONSOLE] {msg.type}: {msg.text}")
        
        # Wait for service worker to be available
        async def wait_for_sw():
            while not context.service_workers:
                await asyncio.sleep(0.1)
            sw = context.service_workers[0]
            sw.on("console", handle_service_worker_console)
            print("✅ Service worker console listener attached")
        
        # Start SW listener in background
        context.on("serviceworker", lambda sw: sw.on("console", handle_service_worker_console))
        
        # 1. Navigate to target site
        print(f"Navigating to {TARGET_URL}...")
        await page.goto(TARGET_URL)
        await page.wait_for_load_state("networkidle")

        # 2. Verify Content Script Injection via global variable (if exposed) or element
        # We check for the sidebar existence or the global function we defined
        print("Checking for content script injection...")
        # Give some time for async module loading
        # Give some time for async module loading
        await asyncio.sleep(2) 
        
        # Try to execute a script that checks for our injected globals 
        # (Note: content script runs in isolated world, but sidebar injects into main world)
        is_sidebar_present = await page.evaluate("""() => {
            return !!document.getElementById('antigravity_sidebar');
        }""")
        
        if is_sidebar_present:
            print("✅ Sidebar detected! Content script is active.")
        else:
            print("⚠️ Sidebar NOT detected yet. Triggering test manually via message simulation...")

        # 3. Trigger the Test Manually (Simulating Popup Message)
        # Since we can't easily click the extension popup in Playwright, 
        # we will simulate the message that the background script sends to the content script.
        # OR we can try to send a message to the runtime if the background script is listening.
        
        # Let's try to find the extension ID first
        service_worker = context.service_workers[0] if context.service_workers else None
        if not service_worker:
            # Wait for background worker
            print("Waiting for extension service worker...")
            # This might not work reliably if worker is lazy loaded, but strict mode should have it.
            # We'll just try to use the first specialized page or just continue.
            pass

        # We can use the background page to send the message
        # Get background pages
        background_pages = context.background_pages
        if not background_pages and not service_worker:
             print("❌ No background page found. Extension might not be loaded correctly.")
        else:
            print("✅ Extension Background loaded.")

        # 4. Programmatically trigger START_TEST by sending message to background
        print("\n🚀 Triggering START_TEST programmatically...")
        
        # Get the extension's service worker context
        if service_worker:
            try:
                # Use CDP to send message to background script
                await service_worker.evaluate("""
                    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                        if (tabs[0]) {
                            chrome.runtime.sendMessage({
                                type: 'START_TEST',
                                payload: {
                                    tabId: tabs[0].id,
                                    goal: 'Login as standard_user, add backpack & bike light to cart, and complete full checkout flow.',
                                    url: 'https://www.saucedemo.com'
                                }
                            });
                        }
                    });
                """)
                # 4. Wait for mission completion and extract logs
                print("\n⏳ Monitoring mission progress...")
                
                max_wait = 180 # 3 minutes
                start_time = asyncio.get_event_loop().time()
                is_finished = False
                
                while (asyncio.get_event_loop().time() - start_time) < max_wait:
                    state = await page.evaluate("() => window.__QA_AGENT_STATE__ || {}")
                    
                    if state.get("isComplete"):
                        print(f"\n🏁 Mission Finished with status: {state.get('lastStatus')}")
                        is_finished = True
                        break
                    
                    if state.get('lastStatus'):
                        print(f"   [AGENT] {state.get('lastStatus')}")
                        
                    await asyncio.sleep(5)
                
                if not is_finished:
                    print("\n⚠️ Mission timed out.")

                # EXTRACT LOGS FOR FEEDBACK BRIDGE
                final_state = await page.evaluate("() => window.__QA_AGENT_STATE__ || {}")
                logs = final_state.get("logs", [])
                
                if logs:
                    log_file = "qa_session_logs.json"
                    with open(log_file, "w") as f:
                        json.dump(final_state, f, indent=2)
                    print(f"✅ Extracted {len(logs)} log entries to {log_file}")
                
            except Exception as e:
                print(f"❌ Error during execution: {e}")
        
        print("\n--- Test Run Complete ---")
        # await asyncio.Event().wait() # Remove blocking wait to allow orchestrator to proceed

if __name__ == "__main__":
    asyncio.run(run())

if __name__ == "__main__":
    asyncio.run(run())
