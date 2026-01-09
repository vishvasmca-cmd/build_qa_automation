from playwright.async_api import Page, expect

class ProductsPage:
    """
    Displays a list of products available for purchase.
    URL Pattern: /products
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_product_input(self):
        """Input field to search for products"""
        return self.page.get_by_placeholder('Search Product').or_(self.page.locator('#search_product'))

    @property
    def search_button(self):
        """Button to submit the product search"""
        return self.page.locator('#submit_search').or_(self.page.get_by_role('button', name='Search'))

    @property
    def category_women_button(self):
        """Button to expand the women category"""
        return self.page.locator('#accordian > div:nth-child(2) > a').or_(self.page.get_by_text('Women'))

    @property
    def category_men_button(self):
        """Button to expand the men category"""
        return self.page.locator('#accordian > div:nth-child(3) > a').or_(self.page.get_by_text('Men'))

    @property
    def category_kids_button(self):
        """Button to expand the kids category"""
        return self.page.locator('#accordian > div:nth-child(4) > a').or_(self.page.get_by_text('Kids'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Automation Exercise - All Products')
        await expect(page.locator('h2', has_text='All Products')).to_be_visible()