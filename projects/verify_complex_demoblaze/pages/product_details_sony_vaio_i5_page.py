from playwright.async_api import Page, expect

class ProductDetailsSonyVaioI5Page:
    """
    This page displays the details of a specific product, in this case, the Sony Vaio i5 laptop. It includes the product name, price, description, and an 'Add to cart' button.
    URL Pattern: https://www.demoblaze.com/prod.html?idp_=8#
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_name(self):
        """The name of the product."""
        return self.page.//h2[text()='Sony vaio i5'].or_(self.page.css=h2)

    @property
    def product_price(self):
        """The price of the product."""
        return self.page.//h3[text()='$790 '].or_(self.page.css=.price-container)

    @property
    def product_description(self):
        """The description of the product."""
        return self.page.//div[@id='more-information'].or_(self.page.css=#more-information)

    @property
    def add_to_cart(self):
        """Button to add the product to the shopping cart."""
        return self.page.//a[text()='Add to cart'].or_(self.page.css=.btn.btn-success.btn-lg)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title contains 'PRODUCT STORE'
        await Verify the product name is 'Sony vaio i5'
        await Verify the 'Add to cart' button is present