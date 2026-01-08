from playwright.async_api import Page, expect

class ProductsPage:
    """
    Displays a list of products with options to add them to the cart or view details
    URL Pattern: /products
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_category_women(self):
        """Button to expand Women category"""
        return self.page.get_by_text('WOMEN').locator('xpath=../button').or_(self.page.locator('xpath=//div[@id='accordian']/div[1]/div[1]/h4/a/button'))

    @property
    def add_to_cart_button(self):
        """Button to add a product to the cart"""
        return self.page.get_by_role('button', name='Add to cart').or_(self.page.locator('.product-overlay > .overlay-content > .add-to-cart'))

    @property
    def view_product_link(self):
        """Link to view the detailed product page"""
        return self.page.get_by_text('+ View Product').or_(self.page.locator('.choose > li > a'))

    @property
    def brand_polo(self):
        """Link to filter by the POLO brand"""
        return self.page.get_by_text('POLO').or_(self.page.locator('a[href="/brand_products/Polo"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Automation Exercise - All Products')
        await expect(page.locator('.features_items').locator('.single-products').first()).to_be_visible()
        await expect(page.get_by_text('All Products')).to_be_visible()