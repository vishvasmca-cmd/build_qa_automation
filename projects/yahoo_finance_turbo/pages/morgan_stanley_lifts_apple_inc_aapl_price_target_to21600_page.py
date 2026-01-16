from playwright.async_api import Page, expect

class MorganStanleyLiftsAppleIncAaplPriceTargetTo21600Page:
    """
    This page displays a financial news article about Morgan Stanley increasing Apple Inc.'s (AAPL) price target.
    URL Pattern: https://finance.yahoo.com/news/morgan-stanley-lifts-apple-inc-*.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for news, tickers, or companies."""
        return self.page.search.or_(self.page.input[placeholder='Search for news, tickers or companies'])

    @property
    def quote_lookup_autocomplete(self):
        """Autocomplete suggestions that appear when typing in the search input."""
        return self.page.Quote Lookup.or_(self.page.div[aria-label='Quote Lookup'])

    @property
    def mail_link(self):
        """Link to the mail section."""
        return self.page.Mail.or_(self.page.a[aria-label='Mail'])

    @property
    def sign_in_link(self):
        """Link to the sign-in page."""
        return self.page.Sign in.or_(self.page.a[data-test-id='uh-sign-in'])

    @property
    def upgrade_to_premium_button(self):
        """Button to upgrade to a premium account."""
        return self.page.Upgrade to Premium.or_(self.page.a[data-test-id='upgrade-button'])

    @property
    def apple_inc_aapl_price_target_article_title(self):
        """The main title of the news article."""
        return self.page.Morgan Stanley Lifts Apple Inc. (AAPL) Price Target on Earnings Growth Expectations.or_(self.page.h1:contains('Morgan Stanley Lifts Apple Inc. (AAPL) Price Target'))

    @property
    def neha_gupta_author(self):
        """The author of the news article."""
        return self.page.Neha Gupta.or_(self.page.span:contains('Neha Gupta'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Morgan Stanley Lifts Apple Inc. (AAPL) Price Target'
        await Article title 'Morgan Stanley Lifts Apple Inc. (AAPL) Price Target on Earnings Growth Expectations' is visible
        await Author 'Neha Gupta' is visible