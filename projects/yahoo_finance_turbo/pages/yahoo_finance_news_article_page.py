from playwright.async_api import Page, expect

class YahooFinanceNewsArticlePage:
    """
    This page displays detailed information about a specific stock (Apple Inc. - AAPL) on Yahoo Finance, including its current price, historical data, news, and related analysis.
    URL Pattern: https://finance.yahoo.com/quote/*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def stock_ticker(self):
        """The stock ticker symbol (e.g., AAPL) displayed as the main heading."""
        return self.page.//h1[contains(text(),'AAPL')].or_(self.page.css=h1)

    @property
    def current_stock_price(self):
        """The current trading price of the stock."""
        return self.page.//fin-streamer[@data-symbol='AAPL' and @data-field='regularMarketPrice'].or_(self.page.css=fin-streamer[data-field='regularMarketPrice'])

    @property
    def follow_button(self):
        """Button to add the stock to the user's portfolio."""
        return self.page.//button[contains(.,'Follow')].or_(self.page.text=Follow)

    @property
    def analyze_with_ai_button(self):
        """Button to analyze the stock with AI."""
        return self.page.//span[contains(text(),'Analyze with AI')].or_(self.page.text=Analyze with AI)

    @property
    def summary_link(self):
        """Link to the summary page of the stock."""
        return self.page.//a[contains(text(),'Summary')].or_(self.page.text=Summary)

    @property
    def news_link(self):
        """Link to the news page of the stock."""
        return self.page.//a[contains(text(),'News')].or_(self.page.text=News)

    @property
    def chart_link(self):
        """Link to the chart page of the stock."""
        return self.page.//a[contains(text(),'Chart')].or_(self.page.text=Chart)

    @property
    def quote_lookup(self):
        """Input field to search for a stock."""
        return self.page.//input[@placeholder='Quote Lookup'].or_(self.page.css=input[placeholder='Quote Lookup'])

    @property
    def upgrade_to_premium(self):
        """Link to upgrade to premium."""
        return self.page.//a[contains(text(),'Upgrade to Premium')].or_(self.page.text=Upgrade to Premium)

    @property
    def got_it(self):
        """Button to close the popup."""
        return self.page.//span[contains(text(),'Got it')].or_(self.page.text=Got it)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'AAPL - Yahoo Finance'
        await Stock ticker (e.g., AAPL) is displayed
        await Current stock price is displayed
        await Follow button is present
        await Summary link is present