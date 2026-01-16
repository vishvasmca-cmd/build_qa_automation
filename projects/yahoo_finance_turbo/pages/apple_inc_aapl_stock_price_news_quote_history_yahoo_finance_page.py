from playwright.async_api import Page, expect

class AppleIncAaplStockPriceNewsQuoteHistoryYahooFinancePage:
    """
    This page displays the stock price, news, quote, history, and other financial information for Apple Inc. (AAPL) on Yahoo Finance.
    URL Pattern: https://finance.yahoo.com/quote/AAPL/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for news, tickers, or companies."""
        return self.page.search-input.or_(self.page.input[placeholder='Search for news, tickers or companies'])

    @property
    def follow_button(self):
        """Button to follow the stock."""
        return self.page.follow-button.or_(self.page.button[aria-label='Follow'])

    @property
    def _1d_time_range(self):
        """Button to select 1 day time range for the stock chart."""
        return self.page.time-range[data-range='1d'].or_(self.page.button[aria-label='1D'])

    @property
    def _5d_time_range(self):
        """Button to select 5 day time range for the stock chart."""
        return self.page.time-range[data-range='5d'].or_(self.page.button[aria-label='5D'])

    @property
    def _1m_time_range(self):
        """Button to select 1 month time range for the stock chart."""
        return self.page.time-range[data-range='1m'].or_(self.page.button[aria-label='1M'])

    @property
    def _6m_time_range(self):
        """Button to select 6 month time range for the stock chart."""
        return self.page.time-range[data-range='6m'].or_(self.page.button[aria-label='6M'])

    @property
    def ytd_time_range(self):
        """Button to select Year-to-Date time range for the stock chart."""
        return self.page.time-range[data-range='ytd'].or_(self.page.button[aria-label='YTD'])

    @property
    def _1y_time_range(self):
        """Button to select 1 year time range for the stock chart."""
        return self.page.time-range[data-range='1y'].or_(self.page.button[aria-label='1Y'])

    @property
    def key_events_dropdown(self):
        """Dropdown to select key events to display on the chart."""
        return self.page.key-events-dropdown.or_(self.page.button[aria-label='Key Events'])

    @property
    def advanced_chart_link(self):
        """Link to view the advanced chart."""
        return self.page.advanced-chart-link.or_(self.page.a[aria-label='Advanced Chart'])

    @property
    def quote_lookup_input(self):
        """Input field to lookup a stock quote."""
        return self.page.quote-lookup-input.or_(self.page.input[placeholder='Quote Lookup'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'AAPL - Finance'
        await Page contains the text 'Apple Inc. (AAPL)'
        await Page contains the element with text 'Summary'
        await Page contains the element with text 'Chart'