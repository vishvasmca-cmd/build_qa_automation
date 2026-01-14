from playwright.sync_api import sync_playwright

def verify_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-http2", "--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to dyson.in...")
        page.goto("https://www.dyson.in/", timeout=60000, wait_until="domcontentloaded")
        
        # Handle popup
        try:
            popup = page.locator("button[aria-label='Close'], button.close, .modal-close").first
            if popup.is_visible(timeout=5000):
                popup.click()
                print("Popup closed.")
        except:
            print("No popup handled.")

        print("Locating search button...")
        # Exact locator from user
        search_btn = page.locator("button[aria-label='Search products and parts'].header__search__input-open")
        search_btn.wait_for(state="visible", timeout=10000)
        search_btn.click()
        print("Clicked search button.")

        print("Waiting for input...")
        # Exact locator from user
        search_input = page.locator("input[placeholder='dyson.in'][type='search']")
        search_input.wait_for(state="visible", timeout=10000)
        
        print("Filling search...")
        search_input.fill("Dyson V15 Detect")
        search_input.press("Enter")
        
        print("Waiting for results...")
        page.wait_for_selector("text=V15", timeout=15000)
        print("SUCCESS: Search results found.")
        
        browser.close()

if __name__ == "__main__":
    verify_search()
