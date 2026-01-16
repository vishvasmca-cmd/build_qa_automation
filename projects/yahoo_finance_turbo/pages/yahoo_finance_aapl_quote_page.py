from playwright.async_api import Page, expect

class YahooFinanceAaplQuotePage:
    """
    This page provides financial information and news related to a specific stock, in this case, Microsoft (MSFT).
    URL Pattern: https://finance.yahoo.com/quote/MSFT/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def learn_more_button(self):
        """Button to learn more about AT&T Business internet."""
        return self.page.role=button[name='Learn more'].or_(self.page.text=Learn more)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'MSFT'
        await Page contains the text 'Microsoft'