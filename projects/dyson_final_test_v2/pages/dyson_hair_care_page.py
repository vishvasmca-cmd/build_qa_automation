from playwright.async_api import Page, expect

class DysonHairCarePage:
    """
    This page is the Dyson Hair Care landing page on the Dyson India website. It showcases Dyson's hair care products and provides links to explore different product categories.
    URL Pattern: https://www.dyson.in/air-treatment
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Hair Care Tab(self):
        """Link to the main Hair Care page."""
        return self.page.role=link[name="Hair care"].or_(self.page.text=Hair care)

    @property
    def Search Products and Parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Shopping Cart Icon(self):
        """Link to the shopping cart."""
        return self.page.role=link[name="Basket"].or_(self.page.css=a[aria-label='Basket'])

    @property
    def Hair Stylers(self):
        """Link to the Hair Stylers product category."""
        return self.page.role=link[name="Hair stylers"].or_(self.page.text=Hair stylers)

    @property
    def Hair Dryers(self):
        """Link to the Hair Dryers product category."""
        return self.page.role=link[name="Hair dryers"].or_(self.page.text=Hair dryers)

    @property
    def Hair Straighteners(self):
        """Link to the Hair Straighteners product category."""
        return self.page.role=link[name="Hair straighteners"].or_(self.page.text=Hair straighteners)

    @property
    def Professional Hair Care(self):
        """Link to the Professional Hair Care product category."""
        return self.page.role=link[name="Professional hair care"].or_(self.page.text=Professional hair care)

    @property
    def Shop All Hair Care(self):
        """Link to view all hair care products."""
        return self.page.role=link[name="Shop all hair care"].or_(self.page.text=Shop all hair care)

    @property
    def Gifts(self):
        """Link to the Gifts product category."""
        return self.page.role=link[name="Gifts"].or_(self.page.text=Gifts)

    @property
    def Cases, Accessories & Attachments(self):
        """Link to the Cases, Accessories & Attachments product category."""
        return self.page.role=link[name="Cases, accessories & attachments"].or_(self.page.text=Cases, accessories & attachments)

    @property
    def Styling Guides(self):
        """Link to the Styling Guides product category."""
        return self.page.role=link[name="Styling guides"].or_(self.page.text=Styling guides)

    @property
    def Hair Science(self):
        """Link to the Hair Science product category."""
        return self.page.role=link[name="Hair science"].or_(self.page.text=Hair science)

    @property
    def Close Promotion(self):
        """Button to close the promotion banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Hair Care'
        await The 'Hair care' tab is highlighted in the navigation bar.
        await The 'Search products and parts' search box is visible.
        await At least one hair care product category link is visible (e.g., 'Hair stylers').