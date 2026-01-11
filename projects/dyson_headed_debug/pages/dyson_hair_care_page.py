from playwright.async_api import Page, expect

class DysonHairCarePage:
    """
    This page is the Dyson Hair Care landing page, showcasing various hair care products and information.
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
        """Search input field for products and parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

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
        """Link to the Gifts section."""
        return self.page.role=link[name="Gifts"].or_(self.page.text=Gifts)

    @property
    def Cases, Accessories & Attachments(self):
        """Link to the Cases, Accessories & Attachments section."""
        return self.page.role=link[name="Cases, accessories & attachments"].or_(self.page.text=Cases, accessories & attachments)

    @property
    def Styling Guides(self):
        """Link to the Styling Guides section."""
        return self.page.role=link[name="Styling guides"].or_(self.page.text=Styling guides)

    @property
    def Hair Science(self):
        """Link to the Hair Science section."""
        return self.page.role=link[name="Hair science"].or_(self.page.text=Hair science)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Hair Care'
        await The 'Hair care' tab is highlighted in the navigation bar.
        await The 'Hair stylers' link is visible.
        await The 'Hair dryers' link is visible.