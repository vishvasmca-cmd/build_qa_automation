from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-http2"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to dyson.in...")
        page.goto("https://www.dyson.in/", timeout=60000, wait_until="commit")
        page.wait_for_load_state("domcontentloaded")
        print("Page loaded.")

        # Handle Popup?
        try:
            # Common popup locators
            popup_close = page.locator("button.close, .modal-close, [aria-label='Close'], button:has-text('No thanks')").first
            if popup_close.is_visible(timeout=5000):
                print("Popup found, closing...")
                popup_close.click()
            else:
                # Dyson specific - maybe a newsletter?
                pass
        except:
            print("No popup handled.")

        # Try to find search
        print("Looking for search...")
        
        # Method 1: Search input directly
        search_input = page.locator("input[type='search'], input[type='text'][placeholder*='Search']")
        if search_input.count() > 0 and search_input.first.is_visible():
            print("Found search input directly.")
            search_input.first.fill("Dyson V15 Detect")
            search_input.first.press("Enter")
            print("Search submitted.")
            return

        # Method 2: Click search icon first
        search_icon = page.locator("button[aria-label='Search'], a[aria-label='Search'], .search-icon, [data-testid='header-search-icon']")
        if search_icon.count() > 0:
            print(f"Found search icon: {search_icon.first}")
            search_icon.first.click()
            time.sleep(1)
            
            search_input = page.locator("input[type='search'], input#search")
            if search_input.is_visible():
                print("Found search input after click.")
                search_input.fill("Dyson V15 Detect")
                search_input.press("Enter")
                print("Search submitted.")
                return
            else:
                print("Clicked icon but input not visible.")

        # Dump info if failed
        print("Failed to find search. Dumping buttons in header...")
        header = page.locator("header")
        if header.count() > 0:
            print(header.first.inner_html())
        
        # Take screenshot
        page.screenshot(path="search_debug.png")
        browser.close()

if __name__ == "__main__":
    run()
