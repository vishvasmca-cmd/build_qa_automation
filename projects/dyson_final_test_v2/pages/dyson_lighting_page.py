from playwright.async_api import Page, expect

class DysonLightingPage:
    """
    This page is dedicated to showcasing Dyson's lighting products and providing information about their features and benefits.
    URL Pattern: https://www.dyson.in/support
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Lighting Navigation Link(self):
        """Link to the main Dyson Lighting page."""
        return self.page.role=link[name="Lighting"].or_(self.page.text=Lighting)

    @property
    def Search Products and Parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

    @property
    def Dyson Solarcycle Morph™ Link(self):
        """Link to the Dyson Solarcycle Morph product page."""
        return self.page.role=link[name="Dyson Solarcycle Morph™"].or_(self.page.text=Dyson Solarcycle Morph™)

    @property
    def Shop lighting Link(self):
        """Link to the Dyson Shop lighting product page."""
        return self.page.role=link[name="Shop lighting"].or_(self.page.text=Shop lighting)

    @property
    def Exclusive Offer Close Button(self):
        """Button to close the exclusive offer banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label="Close"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Lighting'
        await Header text contains 'Lighting'
        await The 'Dyson Solarcycle Morph™' link is visible
        await The 'Shop lighting' link is visible