from playwright.async_api import Page, expect

class DysonAirTreatmentPage:
    """
    This page is the Dyson Air Treatment landing page, specifically focusing on Air Purifiers. It allows users to explore and learn about Dyson's air purifier products.
    URL Pattern: https://www.dyson.in/air-treatment
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Air Purifier Link(self):
        """Link to the Air Purifier section."""
        return self.page.role=link[name="Air purifier"].or_(self.page.text=Air purifier)

    @property
    def Search Products and Parts(self):
        """Search input box to find products and parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

    @property
    def Air Purifiers(self):
        """Link to the Air Purifiers category."""
        return self.page.role=link[name="Air Purifiers"].or_(self.page.text=Air Purifiers)

    @property
    def Purifier + Heaters(self):
        """Link to the Purifier + Heaters category."""
        return self.page.role=link[name="Purifier + Heaters"].or_(self.page.text=Purifier + Heaters)

    @property
    def Shop all air purifiers(self):
        """Link to shop all air purifiers."""
        return self.page.role=link[name="Shop all air purifiers"].or_(self.page.text=Shop all air purifiers)

    @property
    def Exclusive Offer Close Button(self):
        """Button to close the exclusive offer banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=div[aria-label="Close"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Air Treatment'
        await Header contains 'Air purifier'
        await The 'Air Purifiers' link is visible