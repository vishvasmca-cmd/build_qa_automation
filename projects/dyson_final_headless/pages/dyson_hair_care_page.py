from playwright.async_api import Page, expect

class DysonHairCarePage:
    """
    This page is the Dyson Hair Care landing page, showcasing various hair care products and related information.
    URL Pattern: https://www.dyson.in/air-treatment
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Hair Care Navigation Link(self):
        """Link to the main Hair Care section of the website."""
        return self.page.role=link[name="Hair care"].or_(self.page.text=Hair care)

    @property
    def Search Products and Parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Hair Stylers Link(self):
        """Link to the Hair Stylers product category."""
        return self.page.role=link[name="Hair stylers"].or_(self.page.text=Hair stylers)

    @property
    def Hair Dryers Link(self):
        """Link to the Hair Dryers product category."""
        return self.page.role=link[name="Hair dryers"].or_(self.page.text=Hair dryers)

    @property
    def Hair Straighteners Link(self):
        """Link to the Hair Straighteners product category."""
        return self.page.role=link[name="Hair straighteners"].or_(self.page.text=Hair straighteners)

    @property
    def Shop All Hair Care Link(self):
        """Link to view all hair care products."""
        return self.page.role=link[name="Shop all hair care"].or_(self.page.text=Shop all hair care)

    @property
    def Gifts Link(self):
        """Link to the Gifts section."""
        return self.page.role=link[name="Gifts"].or_(self.page.text=Gifts)

    @property
    def Cases, Accessories & Attachments Link(self):
        """Link to the Cases, Accessories & Attachments section."""
        return self.page.role=link[name="Cases, accessories & attachments"].or_(self.page.text=Cases, accessories & attachments)

    @property
    def Close Promotion(self):
        """Button to close the promotion banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Hair Care'
        await The 'Hair care' navigation link is visible
        await The 'Search products and parts' search box is visible
        await At least one hair care product category link is visible (e.g., 'Hair stylers', 'Hair dryers')