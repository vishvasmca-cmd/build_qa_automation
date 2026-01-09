from playwright.async_api import Page, expect

class TestPagesJavascriptTagPage:
    """
    Page displaying links to different apps tagged with JavaScript
    URL Pattern: /pages/basics/alerts-javascript/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def triangle_link(self):
        """Link to the Triangle app"""
        return self.page.get_by_role('link', name='Triangle').or_(self.page.locator('a:has-text("Triangle")'))

    @property
    def 7_char_val_link(self):
        """Link to the 7 Char Val app"""
        return self.page.get_by_role('link', name='7 Char Val').or_(self.page.locator('a:has-text("7 Char Val")'))

    @property
    def customer_login_link(self):
        """Link to the Customer Login | Basic Shopping Cart app"""
        return self.page.get_by_role('link', name='Customer Login | Basic Shopping Cart').or_(self.page.locator('a:has-text("Customer Login | Basic Shopping Cart")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Test Page For Basic JavaScript Alerts')
        await expect(page.locator('h1:has-text("Tag: JavaScript")')).to_be_visible()