from playwright.async_api import Page, expect

class YahooFinanceMarketsPage:
    """
    This page provides news and information on various topics including finance, health, and world events.
    URL Pattern: https://finance.yahoo.com/quote/AAPL/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def learn_more_button(self):
        """Button to learn more about the Mercedes-Benz offer."""
        return self.page.text='LEARN MORE'.or_(self.page.css=a[aria-label='LEARN MORE'])

    @property
    def news_link(self):
        """Link to the News section."""
        return self.page.text='News'.or_(self.page.css=a[href*='/news/'])

    @property
    def health_link(self):
        """Link to the Health section."""
        return self.page.text='Health'.or_(self.page.css=a[href*='/health/'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Yahoo Finance'
        await Presence of 'News' link
        await Presence of 'Health' link