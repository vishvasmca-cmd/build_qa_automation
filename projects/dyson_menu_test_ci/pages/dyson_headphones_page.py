from playwright.async_api import Page, expect

class DysonHeadphonesPage:
    """
    This page is the landing page for Dyson Headphones, specifically the 'ontrac' model. It showcases the product and provides a 'Shop now' call to action.
    URL Pattern: https://www.dyson.in/lighting
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def shop_now_button(self):
        """Button to navigate to the product page or add the headphones to the cart."""
        return self.page.text=Shop now.or_(self.page.css=a[href*='/headphones/'])

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def headphones_navigation_link(self):
        """Link to the headphones category page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def close_promotion_banner(self):
        """Button to close the promotion banner at the bottom of the page."""
        return self.page.text=X.or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header text 'ontrac Headphones, remastered' is present
        await The 'Shop now' button is visible
        await The promotion banner is displayed