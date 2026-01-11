from playwright.async_api import Page, expect

class DysonLightingPage:
    """
    This page displays information about Dyson's lighting products. It allows users to explore different lighting options and learn about their features.
    URL Pattern: https://www.dyson.in/support
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Lighting Tab(self):
        """Link to the main lighting product page."""
        return self.page.role=link[name="Lighting"].or_(self.page.text=Lighting)

    @property
    def Search Products and Parts(self):
        """Search input field for products and parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=.search-input)

    @property
    def Dyson Solarcycle Morph(self):
        """Link to the Dyson Solarcycle Morph product page."""
        return self.page.role=link[name="Dyson Solarcycle Morph™"].or_(self.page.text=Dyson Solarcycle Morph™)

    @property
    def Shop lighting(self):
        """Link to the shop lighting page."""
        return self.page.role=link[name="Shop lighting"].or_(self.page.text=Shop lighting)

    @property
    def Sure, I'll give feedback(self):
        """Button to provide feedback."""
        return self.page.role=button[name="Sure, I'll give feedback"].or_(self.page.text=Sure, I'll give feedback)

    @property
    def No thanks(self):
        """Button to decline providing feedback."""
        return self.page.role=button[name="No thanks"].or_(self.page.text=No thanks)

    @property
    def Close Reward Points Banner(self):
        """Button to close the reward points banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=.close-button)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Lighting'
        await Page contains the heading 'Lighting'
        await Page contains the text 'Dyson lighting is engineered for task performance with precise colour accuracy, daylight tracking and shadow reduction, ensuring accurate creative work is supported.'