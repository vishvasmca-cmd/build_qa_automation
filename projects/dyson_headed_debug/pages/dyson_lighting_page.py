from playwright.async_api import Page, expect

class DysonLightingPage:
    """
    This page displays information about Dyson Lighting products and related support.
    URL Pattern: https://www.dyson.in/support
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Lighting Link(self):
        """Link to the Dyson Lighting product page."""
        return self.page.role=link[name="Lighting"].or_(self.page.text=Lighting)

    @property
    def Search Products and Parts(self):
        """Search input box to find products and parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

    @property
    def Dyson Solarcycle Morph(self):
        """Link to the Dyson Solarcycle Morph product page."""
        return self.page.role=link[name="Dyson Solarcycle Morph™"].or_(self.page.text="Dyson Solarcycle Morph™")

    @property
    def Shop lighting(self):
        """Link to the Dyson shop lighting page."""
        return self.page.role=link[name="Shop lighting"].or_(self.page.text="Shop lighting")

    @property
    def Sure, I'll give feedback(self):
        """Button to provide feedback."""
        return self.page.text="Sure, I'll give feedback".or_(self.page.css=button[class*='feedback'])

    @property
    def No thanks(self):
        """Button to decline providing feedback."""
        return self.page.text="No thanks".or_(self.page.css=button[class*='no-thanks'])

    @property
    def Close Exclusive Offer(self):
        """Button to close the exclusive offer banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label="Close"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Lighting'
        await Header text contains 'Lighting'
        await The 'Search products and parts' search box is present