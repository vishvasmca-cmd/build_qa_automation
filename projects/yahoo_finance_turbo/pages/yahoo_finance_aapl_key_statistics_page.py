from playwright.async_api import Page, expect

class YahooFinanceAaplKeyStatisticsPage:
    """
    This page displays the key statistics for Apple Inc. (AAPL) on Yahoo Finance. It provides financial metrics and ratios to assess the company's performance and valuation.
    URL Pattern: https://finance.yahoo.com/quote/AAPL/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def play_video(self):
        """Button to play the video."""
        return self.page.role=button[name='Play'].or_(self.page.css=button[aria-label='Play'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'AAPL - Key Statistics'
        await Page contains the header 'Key Statistics'