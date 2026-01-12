from playwright.async_api import Page, expect

class DemoblazePage:
    """
    This page displays the details of a specific product on the Demoblaze e-commerce site.
    URL Pattern: https://www.demoblaze.com/prod.html?idp_=
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_title(self):
        """The title of the product being displayed."""
        return self.page.//h2[@class='name'].or_(self.page.h2.name)

    @property
    def product_price(self):
        """The price of the product."""
        return self.page.//h3[@class='price-container'].or_(self.page.h3.price-container)

    @property
    def product_description(self):
        """Detailed description of the product."""
        return self.page.//div[@id='more-information'].or_(self.page.#more-information)

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.//a[contains(text(),'Add to cart')].or_(self.page.a.btn.btn-success.btn-lg)

    @property
    def product_image(self):
        """Main image of the product."""
        return self.page.//img[@class='d-block img-fluid'].or_(self.page.img.d-block.img-fluid)

    @property
    def categories_phones(self):
        """Link to navigate to the phones category."""
        return self.page.//a[contains(text(),'Phones')].or_(self.page.#itemc)

    @property
    def categories_laptops(self):
        """Link to navigate to the laptops category."""
        return self.page.//a[contains(text(),'Laptops')].or_(self.page.#itemc)

    @property
    def categories_monitors(self):
        """Link to navigate to the monitors category."""
        return self.page.//a[contains(text(),'Monitors')].or_(self.page.#itemc)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the product title is displayed.
        await Verify that the product price is displayed.
        await Verify that the product description is displayed.
        await Verify that the 'Add to cart' button is present.
        await Verify that the product image is displayed.