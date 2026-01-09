from playwright.async_api import Page, expect

class TestPagesJavascriptTagsPage:
    """
    Page displaying links to apps tagged with JavaScript.
    URL Pattern: /tags/javascript/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def triangle_link(self):
        """Link to the Triangle app."""
        return self.page.get_by_role('link', name='Triangle').or_(self.page.locator('a', has_text='Triangle'))

    @property
    def 7_char_val_link(self):
        """Link to the 7 Char Val app."""
        return self.page.get_by_role('link', name='7 Char Val').or_(self.page.locator('a', has_text='7 Char Val'))

    @property
    def customer_login_link(self):
        """Link to the Customer Login | Basic Shopping Cart app."""
        return self.page.get_by_role('link', name='Customer Login | Basic Shopping Cart').or_(self.page.locator('a', has_text='Customer Login | Basic Shopping Cart'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Test Page For JavaScript Tags')
        await expect(page.get_by_role('heading', name='Tag: JavaScript')).to_be_visible()