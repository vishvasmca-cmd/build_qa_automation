from playwright.async_api import Page, expect

class ProductsPage:
    """
    This page allows the user to select items to add to their Dyson OnTrac bundle.
    URL Pattern: https://www.dyson.in/checkout/cart/configure/id/109287037/product_id/57385/variant/%5B%5D/action/add/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def ontrac_ear_cushions_khaki_(self):
        """The OnTrac ear cushions product."""
        return self.page.text="OnTrac™ ear cushions (Khaki)".or_(self.page.css=div:nth-child(1) > div > div.product-name)

    @property
    def ontrac_outer_caps_cnc_copper_(self):
        """The OnTrac outer caps product."""
        return self.page.text="OnTrac™ outer caps (CNC Copper)".or_(self.page.css=div:nth-child(2) > div > div.product-name)

    @property
    def continue_to_basket_top_(self):
        """Button to continue to the basket from the top of the page."""
        return self.page.text="Continue to basket".or_(self.page.css=.cart-page-header > div > a)

    @property
    def continue_to_basket_bottom_(self):
        """Button to continue to the basket from the bottom of the page."""
        return self.page.text="Continue to basket".or_(self.page.css=.cart-page-summary > div > a)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header text is 'Select your items'
        await Total price is displayed