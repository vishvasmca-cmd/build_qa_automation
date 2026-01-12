from playwright.async_api import Page, expect

class DysonAirstraitStraightenerPage:
    """
    This page is a product detail page for the Dyson Airstrait hair straightener in pink and gold. It provides information about the product and allows users to purchase it.
    URL Pattern: https://www.dyson.in/airstrait-hair-straightener-pink-gold
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.role=button[name='Add to cart'].or_(self.page.css=button.button--primary)

    @property
    def buy_now_button(self):
        """Button to directly purchase the product."""
        return self.page.role=button[name='Buy now'].or_(self.page.text=Buy now)

    @property
    def product_title(self):
        """The main title of the product on the page."""
        return self.page.role=heading[level=1].or_(self.page.css=h1.product-title)

    @property
    def product_image(self):
        """The main image of the Dyson Airstrait straightener."""
        return self.page.role=img[alt='Dyson Airstrait straightener'].or_(self.page.css=img.product-image)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Airstrait straightener'
        await Page contains the product title
        await Page contains the 'Add to cart' button
        await Page contains the 'Buy now' button