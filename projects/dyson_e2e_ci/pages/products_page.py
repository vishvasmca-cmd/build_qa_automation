from playwright.async_api import Page, expect

class ProductsPage:
    """
    This page allows the user to select additional items to bundle with the Dyson V8 Absolute vacuum cleaner. It displays available items and allows the user to add them to their basket.
    URL Pattern: https://www.dyson.in/checkout/cart/configure/id/109288945/product_id/37342/variant/%5B%5D/action/add/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def pet_grooming_kit(self):
        """The Pet Grooming Kit option to add to the bundle."""
        return self.page.text=Pet grooming kit.or_(self.page.css=div:nth-child(1) > div > div > div.product-name)

    @property
    def detail_cleaning_kit(self):
        """The Detail Cleaning Kit option to add to the bundle."""
        return self.page.text=Detail cleaning kit.or_(self.page.css=div:nth-child(2) > div > div > div.product-name)

    @property
    def continue_to_basket_bottom_(self):
        """Button to proceed to the basket with selected items."""
        return self.page.text=Continue to basket.or_(self.page.css=.product-summary > div.actions > button)

    @property
    def continue_to_basket_top_(self):
        """Button to proceed to the basket with selected items."""
        return self.page.text=Continue to basket.or_(self.page.css=.cart-summary > div > button)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Configure your product'
        await Page contains the text 'Select your items'
        await The 'Continue to basket' button is present
        await The price displayed matches the expected price for the base product