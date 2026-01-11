from playwright.async_api import Page, expect

class DysonLightingPage:
    """
    This page is dedicated to showcasing and providing information about Dyson's lighting products.
    URL Pattern: https://www.dyson.in/lighting
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Products and Parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Lighting Tab(self):
        """Link to the main lighting product page."""
        return self.page.role=link[name='Lighting'].or_(self.page.text=Lighting)

    @property
    def Dyson Solarcycle Morph(self):
        """Link to the Dyson Solarcycle Morph product page."""
        return self.page.role=link[name='Dyson Solarcycle Morph™'].or_(self.page.text='Dyson Solarcycle Morph™')

    @property
    def Shop lighting(self):
        """Link to the shop lighting product page."""
        return self.page.role=link[name='Shop lighting'].or_(self.page.text='Shop lighting')

    @property
    def Exclusive Offer Close Button(self):
        """Button to close the exclusive offer banner."""
        return self.page.role=button[name='Close'].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Lighting'
        await Header text 'Lighting' is present
        await Dyson Solarcycle Morph link is present
        await Shop lighting link is present