from playwright.async_api import Page, expect

class DysonHeadphonesPage:
    """
    This page is the Dyson Headphones landing page, showcasing the OnTrac headphones and related accessories.
    URL Pattern: https://www.dyson.in/lighting
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Headphones Navigation Link(self):
        """Link to the Headphones category page."""
        return self.page.role=link[name="Headphones"].or_(self.page.text=Headphones)

    @property
    def OnTrac Headphones Link(self):
        """Link to the OnTrac headphones product page."""
        return self.page.role=link[name="OnTrac™ headphones"].or_(self.page.text=OnTrac™ headphones)

    @property
    def Ear cushions & caps Link(self):
        """Link to the Ear cushions & caps product page."""
        return self.page.role=link[name="Ear cushions & caps"].or_(self.page.text=Ear cushions & caps)

    @property
    def Shop now Button(self):
        """Button to navigate to the product details page."""
        return self.page.role=button[name="Shop now"].or_(self.page.text=Shop now)

    @property
    def Search products and parts(self):
        """Search input field"""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

    @property
    def Close Reward Points Banner(self):
        """Button to close the reward points banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label="Close"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Headphones'
        await Header text contains 'ontrac Headphones, remastered'
        await The 'Shop now' button is visible