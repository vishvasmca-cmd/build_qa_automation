from playwright.async_api import Page, expect

class MorganStanleyLiftsAppleIncAaplPriceTargetOnEarningsGrowthExpectationsYahooFinancePage:
    """
    This page displays a financial news article from Yahoo Finance about Morgan Stanley increasing Apple's price target. It includes the article text, author information, related stock tickers, and related articles.
    URL Pattern: https://finance.yahoo.com/news/*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for news, tickers, or companies."""
        return self.page.Search for news, tickers or companies.or_(self.page.input[type='text'])

    @property
    def article_title(self):
        """The main title of the financial news article."""
        return self.page.Morgan Stanley Lifts Apple Inc. (AAPL) Price Target on Earnings Growth Expectations.or_(self.page.h1)

    @property
    def author_name(self):
        """The name of the author of the article."""
        return self.page.Neha Gupta.or_(self.page.span[class*='name'])

    @property
    def apple_ticker_link(self):
        """Link to the Apple stock ticker page."""
        return self.page.AAPL -0.69% ☆.or_(self.page.a[href*='/quote/AAPL'])

    @property
    def upgrade_to_premium_button(self):
        """Button to upgrade to Yahoo Finance Premium."""
        return self.page.Upgrade to Premium.or_(self.page.a[class*='premium'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Morgan Stanley Lifts Apple Inc. (AAPL) Price Target'
        await Article title 'Morgan Stanley Lifts Apple Inc. (AAPL) Price Target on Earnings Growth Expectations' is present
        await Author name 'Neha Gupta' is present