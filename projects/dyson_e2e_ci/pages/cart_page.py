from playwright.async_api import Page, expect

class CartPage:
    """
    This is the homepage of Dyson India. The primary purpose is to showcase products and promotions.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def cart_icon(self):
        """Link to the shopping cart page."""
        return self.page.role=link[name='Basket'].or_(self.page.css=a[aria-label='Basket'])

    @property
    def shop_now(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=a[aria-label='Shop now'])

    @property
    def close_promotion(self):
        """Button to close the promotion banner."""
        return self.page.aria-label=Close.or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the element 'Search products and parts'