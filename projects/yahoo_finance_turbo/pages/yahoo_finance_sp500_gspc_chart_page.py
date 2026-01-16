from playwright.async_api import Page, expect

class YahooFinanceSP500GspcChartPage:
    """
    This page displays the Yahoo Finance chart for the S&P 500 index (^GSPC), along with related financial data, trending tickers, and watchlist options.
    URL Pattern: https://finance.yahoo.com/chart/%5EGSPC/#eyJsYXlvdXQiOnsi...
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def quote_lookup_input(self):
        """Input field to search for a specific stock symbol or company."""
        return self.page.role=textbox[name='Search'].or_(self.page.css=input[placeholder='Try a valid symbol or a specific company name'])

    @property
    def follow_button(self):
        """Button to follow the S&P 500 index."""
        return self.page.text=Follow.or_(self.page.css=button[aria-label='Follow ^GSPC'])

    @property
    def chart(self):
        """The main chart displaying the S&P 500 index performance over time."""
        return self.page.css=div[class*='chart-canvas'].or_(self.page.alt=Interactive chart)

    @property
    def time_interval_1_day(self):
        """Button to set the chart time interval to 1 day."""
        return self.page.text=1D.or_(self.page.css=span[data-value='1d'])

    @property
    def sign_in_button(self):
        """Button to sign in to view watchlists."""
        return self.page.text=Sign In.or_(self.page.css=button[data-test='signIn'])

    @property
    def trending_tickers_section(self):
        """Section displaying trending tickers."""
        return self.page.text=Trending Tickers >.or_(self.page.css=div[aria-label='Trending Tickers'])

    @property
    def customize_button(self):
        """Button to customize the My Portfolio & Markets section."""
        return self.page.text=Customize.or_(self.page.css=a[title='Customize My Portfolio & Markets'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'S&P 500 (^GSPC) Interactive Stock Chart - Yahoo Finance'
        await Chart is displayed
        await Trending Tickers section is displayed
        await Yahoo Finance logo is visible