from playwright.async_api import Page, expect

class AaplAppleIncStockPriceNewsYahooFinancePage:
    """
    This page displays the stock price, news, and related information for Apple Inc. (AAPL) on Yahoo Finance.
    URL Pattern: https://finance.yahoo.com/quote/AAPL/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for news, tickers, or companies."""
        return self.page.Search for news, tickers or companies.or_(self.page.input[type='search'])

    @property
    def follow_button(self):
        """Button to follow Apple Inc. stock."""
        return self.page.☆ Follow.or_(self.page.button[aria-label='Follow Apple Inc.'])

    @property
    def chart(self):
        """Interactive chart displaying the stock price over time."""
        return self.page.canvas.or_(self.page.div[class*='chart-canvas'])

    @property
    def got_it_button(self):
        """Button to close the AI analysis popup."""
        return self.page.Got it.or_(self.page.button[aria-label='Got it'])

    @property
    def upgrade_to_premium(self):
        """Link to upgrade to Yahoo Finance Premium."""
        return self.page.Upgrade to Premium.or_(self.page.a[href*='/premium/'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'AAPL - Apple Inc. - Stock Price & News - Yahoo Finance'
        await Page contains the header 'Apple Inc. (AAPL)'
        await Page contains the element 'Summary'
        await Page contains the current stock price