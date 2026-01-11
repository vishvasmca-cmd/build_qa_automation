from playwright.async_api import Page, expect

class DysonAirTreatmentPage:
    """
    This page is the Dyson Air Treatment landing page, focusing on air purifiers and related products.
    URL Pattern: https://www.dyson.in/headphones
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Air Purifier Link(self):
        """Link to the Air Purifier product category page."""
        return self.page.role=link[name="Air purifier"].or_(self.page.text=Air purifier)

    @property
    def Search Products and Parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

    @property
    def Air Purifiers(self):
        """Link to the Air Purifiers product listing page."""
        return self.page.role=link[name="Air Purifiers"].or_(self.page.text=Air Purifiers)

    @property
    def Purifier + Heaters(self):
        """Link to the Purifier + Heaters product listing page."""
        return self.page.role=link[name="Purifier + Heaters"].or_(self.page.text=Purifier + Heaters)

    @property
    def Shop all air purifiers(self):
        """Link to the Shop all air purifiers product listing page."""
        return self.page.role=link[name="Shop all air purifiers"].or_(self.page.text=Shop all air purifiers)

    @property
    def Close Promotion(self):
        """Button to close the promotion banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label="Close"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header includes 'Air purifier'
        await The 'Air Purifiers' link is visible
        await The 'Search products and parts' search box is visible