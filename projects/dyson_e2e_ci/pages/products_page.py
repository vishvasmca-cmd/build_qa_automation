from playwright.async_api import Page, expect

class ProductsPage:
    """
    This page allows the user to select items to customize their Dyson OnTrac™ (CNC Copper) product. It displays available items, their descriptions, and prices. The user can then add these items to their basket.
    URL Pattern: https://www.dyson.in/checkout/cart/configure/id/109050766/product_id/57385/variant/%5B%5D/action/add/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def ontrac_ear_cushions_khaki_(self):
        """Link to the OnTrac™ ear cushions (Khaki) product details."""
        return self.page.text=OnTrac™ ear cushions (Khaki).or_(self.page.css=div:nth-child(1) > div > div.product-name)

    @property
    def ontrac_outer_caps_cnc_copper_(self):
        """Link to the OnTrac™ outer caps (CNC Copper) product details."""
        return self.page.text=OnTrac™ outer caps (CNC Copper).or_(self.page.css=div:nth-child(2) > div > div.product-name)

    @property
    def continue_to_basket_top_(self):
        """Button to proceed to the basket/checkout page."""
        return self.page.text=Continue to basket.or_(self.page.css=.button.action.primary.continue)

    @property
    def continue_to_basket_bottom_(self):
        """Button to proceed to the basket/checkout page."""
        return self.page.text=Continue to basket.or_(self.page.css=.button.action.primary.continue)

    @property
    def close_exclusive_offer(self):
        """Button to close the exclusive offer popup."""
        return self.page.text=X.or_(self.page.css=.message-close)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header text is 'Select your items'
        await Total price is displayed
        await Continue to basket button is present