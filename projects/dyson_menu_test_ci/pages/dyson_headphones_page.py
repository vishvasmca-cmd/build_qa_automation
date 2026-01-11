from playwright.async_api import Page, expect

class DysonHeadphonesPage:
    """
    This page is the Dyson Headphones landing page, showcasing the OnTrac headphones.
    URL Pattern: https://www.dyson.in/lighting
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Headphones Link(self):
        """Link to the Headphones section of the website."""
        return self.page.role=link[name="Headphones"].or_(self.page.text=Headphones)

    @property
    def Search Products and Parts(self):
        """Search input field to search for products and parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def OnTrac Headphones Link(self):
        """Link to the OnTrac headphones product page."""
        return self.page.role=link[name="OnTrac™ headphones"].or_(self.page.text=OnTrac™ headphones)

    @property
    def Shop Now Button(self):
        """Button to navigate to the product purchase page."""
        return self.page.role=button[name="Shop now"].or_(self.page.text=Shop now)

    @property
    def Sure, I'll give feedback(self):
        """Button to provide feedback."""
        return self.page.role=button[name="Sure, I'll give feedback"].or_(self.page.text=Sure, I'll give feedback)

    @property
    def No thanks(self):
        """Link to decline providing feedback."""
        return self.page.role=link[name="No thanks"].or_(self.page.text=No thanks)

    @property
    def Dyson Privacy Policy(self):
        """Link to the Dyson Privacy Policy page."""
        return self.page.role=link[name="Dyson Privacy Policy"].or_(self.page.text=Dyson Privacy Policy)

    @property
    def Close Exclusive Offer(self):
        """Button to close the exclusive offer banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header includes 'Headphones'
        await The 'OnTrac™ headphones' link is visible
        await The 'Shop now' button is visible