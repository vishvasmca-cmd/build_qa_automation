from playwright.async_api import Page, expect

class DysonHeadphonesPage:
    """
    This page is the Dyson Headphones landing page, showcasing and promoting their 'OnTrac' headphones.
    URL Pattern: https://www.dyson.in/lighting
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Headphones Link(self):
        """Link to the main Headphones category page."""
        return self.page.role=link[name='Headphones'].or_(self.page.text=Headphones)

    @property
    def OnTrac Headphones Link(self):
        """Link to the OnTrac headphones product page."""
        return self.page.role=link[name='OnTrac™ headphones'].or_(self.page.text=OnTrac™ headphones)

    @property
    def Shop Now Button(self):
        """Button to navigate to the product details page for the featured headphones."""
        return self.page.role=button[name='Shop now'].or_(self.page.text=Shop now)

    @property
    def Ear cushions & caps Link(self):
        """Link to the Ear cushions & caps product page."""
        return self.page.role=link[name='Ear cushions & caps'].or_(self.page.text=Ear cushions & caps)

    @property
    def Search Products and Parts(self):
        """Search input field to search for products and parts."""
        return self.page.role=searchbox[name='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Close Promotion(self):
        """Button to close the promotion banner."""
        return self.page.role=button[name='Close'].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header text 'ontrac Headphones, remastered' is present
        await The 'Shop now' button is visible
        await The 'OnTrac™ headphones' link is visible