from playwright.async_api import Page, expect

class YahooFinanceMsftQuotePage:
    """
    This page displays the quote details for Microsoft Corporation (MSFT) on Yahoo Finance. It includes real-time stock price, historical data, related news, and analysis.
    URL Pattern: https://finance.yahoo.com/quote/AAPL/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for stocks, news, or companies."""
        return self.page.search-quotes.or_(self.page.input[placeholder='Search for news, tickers or companies'])

    @property
    def quote_lookup(self):
        """Container for quote lookup suggestions."""
        return self.page.Quote Lookup.or_(self.page.div[aria-label='Quote Lookup'])

    @property
    def stock_price(self):
        """The current stock price of the company."""
        return self.page.data-test='quote-header-price'.or_(self.page.fin-streamer[data-field='regularMarketPrice'])

    @property
    def stock_change(self):
        """The change in stock price."""
        return self.page.data-test='quote-header-change'.or_(self.page.fin-streamer[data-field='regularMarketChange'])

    @property
    def stock_percent_change(self):
        """The percentage change in stock price."""
        return self.page.data-test='quote-header-percent-change'.or_(self.page.fin-streamer[data-field='regularMarketChangePercent'])

    @property
    def summary_link(self):
        """Link to the summary page."""
        return self.page.Summary.or_(self.page.a[href*='/quote/AAPL?p=AAPL'])

    @property
    def chart_link(self):
        """Link to the chart page."""
        return self.page.Chart.or_(self.page.a[href*='/chart?s=AAPL'])

    @property
    def advanced_chart(self):
        """Link to the advanced chart page."""
        return self.page.Advanced Chart.or_(self.page.a[href*='/chart?s=AAPL&ql=1'])

    @property
    def follow_button(self):
        """Button to follow the stock."""
        return self.page.Follow.or_(self.page.button[aria-label='Follow Microsoft Corporation'])

    @property
    def got_it(self):
        """Button to close the popup."""
        return self.page.Got it.or_(self.page.button[aria-label='Got it'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'AAPL - Yahoo Finance'
        await Page contains the header 'Microsoft Corporation (MSFT)'
        await Stock price is displayed
        await Stock change is displayed
        await Stock percentage change is displayed