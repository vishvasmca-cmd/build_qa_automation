from playwright.async_api import Page, expect

class GoogleFinancePage:
    """
    Google Finance page provides financial information, market data, and news.
    URL Pattern: https://www.google.com/finance/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for stocks, ETFs, or other financial instruments."""
        return self.page.//input[@aria-label='Search'].or_(self.page.input[type='text'])

    @property
    def sign_in_link(self):
        """Link to sign in to a Google account."""
        return self.page.//a[text()='Sign in'].or_(self.page.a[href*='accounts.google.com'])

    @property
    def create_portfolio_button(self):
        """Button to create a new portfolio."""
        return self.page.//a[text()='Create portfolio'].or_(self.page.a[href*='/portfolio/create'])

    @property
    def create_watchlist_button(self):
        """Button to create a new watchlist."""
        return self.page.//a[text()='Create watchlist'].or_(self.page.a[href*='/watchlist/create'])

    @property
    def nvidia_corp_link(self):
        """Link to the NVIDIA Corp stock quote page."""
        return self.page.//a[text()='NVIDIA Corp'].or_(self.page.a[href*='/quote/NVDA'])

    @property
    def intel_corp_link(self):
        """Link to the Intel Corp stock quote page."""
        return self.page.//a[text()='Intel Corp'].or_(self.page.a[href*='/quote/INTC'])

    @property
    def settings_link(self):
        """Link to the settings page."""
        return self.page.//a[text()='Settings'].or_(self.page.a[href*='/settings'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Finance - Google Finance'
        await Search input is present
        await Sign in link is present
        await At least one stock quote link is present (e.g., NVIDIA Corp)