from playwright.async_api import Page, expect

class YahooFinanceMarketsPage:
    """
    This page displays a list of market categories and related news/information.
    URL Pattern: https://finance.yahoo.com/markets/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def markets_link(self):
        """Link to the main markets page."""
        return self.page.text=Markets.or_(self.page.css=a[href='/markets/'])

    @property
    def stocks_link(self):
        """Link to the stocks page."""
        return self.page.text=Stocks.or_(self.page.css=a[href='/topic/stock-market-news/'])

    @property
    def most_active_link(self):
        """Link to the most active stocks page."""
        return self.page.text=Most active.or_(self.page.css=a[href='/most-active'])

    @property
    def day_gainers_link(self):
        """Link to the day gainers page."""
        return self.page.text=Day gainers.or_(self.page.css=a[href='/day-gainers'])

    @property
    def day_losers_link(self):
        """Link to the day losers page."""
        return self.page.text=Day losers.or_(self.page.css=a[href='/day-losers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Markets - Yahoo Finance'
        await The 'Markets' link is visible
        await The 'Stocks' link is visible