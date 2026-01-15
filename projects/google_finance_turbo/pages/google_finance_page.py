from playwright.async_api import Page, expect

class GoogleFinancePage:
    """
    Google Finance provides real-time stock quotes, international market data, news, and financial information.
    URL Pattern: https://www.google.com/finance/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for stocks, ETFs, and other financial instruments."""
        return self.page.role=searchbox.or_(self.page.css=input[aria-label='Search for stocks, ETFs & more'])

    @property
    def sign_in_button(self):
        """Button to sign in to Google Finance."""
        return self.page.text=Sign in.or_(self.page.css=a[href*='signin'])

    @property
    def finance_link(self):
        """Link to the main Finance page."""
        return self.page.text=Finance.or_(self.page.css=a[href='/finance'])

    @property
    def market_trends_link(self):
        """Link to the Market Trends page."""
        return self.page.text=Market trends.or_(self.page.css=a[href*='market_trends'])

    @property
    def create_portfolio_link(self):
        """Link to create a new portfolio."""
        return self.page.text=Create portfolio.or_(self.page.css=a[href*='portfolio'])

    @property
    def create_watchlist_link(self):
        """Link to create a new watchlist."""
        return self.page.text=Create watchlist.or_(self.page.css=a[href*='watchlist'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Google Finance'
        await Search input field is present
        await Sign in button is present
        await Finance link is present