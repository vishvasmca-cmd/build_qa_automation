from playwright.sync_api import Page, Locator, expect

class BasePage:
    """
    Base Page Object class that all other pages inherit from.
    Contains common methods and the shared Page instance.
    """
    def __init__(self, page: Page):
        """Initialize with a Playwright Page instance."""
        self.page = page

    def navigate(self, url: str):
        """Navigate to the specified URL and remove intrusive ads."""
        self.page.goto(url, wait_until="load")
        self.remove_ads()

    def remove_ads(self):
        """Inject JS to remove common ad containers that block clicks."""
        try:
            self.page.evaluate('''() => {
                const selectors = [
                    'iframe[id*="google_ads"]',
                    'ins.adsbygoogle',
                    '#aswift_0_expand',
                    '.ad-slot',
                    '[id*="ad-unit"]'
                ];
                selectors.forEach(s => {
                    const elements = document.querySelectorAll(s);
                    elements.forEach(el => el.remove());
                });
            }''')
        except:
            pass # Ignore if injection fails (e.g. navigation already happened)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()
