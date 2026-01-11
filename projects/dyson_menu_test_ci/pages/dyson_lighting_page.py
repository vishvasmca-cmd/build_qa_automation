from playwright.async_api import Page, expect

class DysonLightingPage:
    """
    This page displays information about Dyson Lighting products.
    URL Pattern: https://www.dyson.in/support
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def lighting_navigation_link(self):
        """Link to the main Lighting product page."""
        return self.page.role=link[name='Lighting'].or_(self.page.text=Lighting)

    @property
    def dyson_solarcycle_morph_link(self):
        """Link to the Dyson Solarcycle Morph product page."""
        return self.page.role=link[name='Dyson Solarcycle Morph™'].or_(self.page.text='Dyson Solarcycle Morph™')

    @property
    def shop_lighting_link(self):
        """Link to the Shop lighting product page."""
        return self.page.role=link[name='Shop lighting'].or_(self.page.text='Shop lighting')

    @property
    def exclusive_reward_points_banner_close_button(self):
        """Button to close the exclusive reward points banner."""
        return self.page.role=button[name='Close'].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Lighting'
        await Header text 'Lighting' is visible
        await Dyson lighting is engineered for task performance with precise colour accuracy, daylight tracking and shadow reduction, ensuring accurate creative work is supported.