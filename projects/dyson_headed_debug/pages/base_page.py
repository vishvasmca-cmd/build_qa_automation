from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def close_popup(self):
        try:
            # Common close button patterns for Dyson / typical overlays
            self.page.locator("text=X").click(timeout=5000)
        except Exception:
            pass

    def navigate_to_url(self, url):
        self.page.goto(url, wait_until="domcontentloaded")
