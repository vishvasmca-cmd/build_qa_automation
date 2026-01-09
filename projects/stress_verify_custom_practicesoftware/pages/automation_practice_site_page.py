from playwright.async_api import Page, expect

class AutomationPracticeSitePage:
    """
    Home page for an e-commerce site selling Selenium books.
    URL Pattern: /
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def my_account_link(self):
        """Link to the My Account page."""
        return self.page.get_by_role('link', name='My Account').or_(self.page.locator('a[href="https://practice.automationtesting.in/my-account/"]'))

    @property
    def shop_link(self):
        """Link to the Shop page."""
        return self.page.get_by_role('link', name='Shop').or_(self.page.locator('a[href="https://practice.automationtesting.in/shop/"]'))

    @property
    def cart_link(self):
        """Link to the shopping cart."""
        return self.page.get_by_role('link', name='0 Items - P0.00').or_(self.page.locator('a[href*="cart"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Automation Practice – Automation Practice')
        await expect(page.locator('text=Shop SELENIUM BOOKS')).to_be_visible()