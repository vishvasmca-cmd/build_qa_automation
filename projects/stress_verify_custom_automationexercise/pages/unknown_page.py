from playwright.async_api import Page, expect

class UnknownPage:
    """
    Search results page for products
    URL Pattern: /products\?search=
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field for searching products"""
        return self.page.get_by_role('textbox').or_(self.page.locator('input#search_product'))

    @property
    def search_button(self):
        """Button to submit the search query"""
        return self.page.get_by_role('button').or_(self.page.locator('#search_product > .fa.fa-search'))

    @property
    def products_link(self):
        """Link to the products page"""
        return self.page.get_by_role('link', name='Products').or_(self.page.locator('a[href="/products"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Automation Exercise - All Products')
        await expect(page.locator('div.features_items').locator('div.col-sm-4').first()).to_be_visible()
        await expect(page.locator('h2', has_text='Searched Products')).to_be_visible()