from playwright.async_api import Page, expect

class DysonAirTreatmentPage:
    """
    This page is the Dyson Air Treatment landing page, showcasing air purifiers and related information.
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
        """Search input field to search for products and parts."""
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
        """Link to shop all air purifiers."""
        return self.page.role=link[name="Shop all air purifiers"].or_(self.page.text=Shop all air purifiers)

    @property
    def Help me choose(self):
        """Link to help me choose a purifier."""
        return self.page.role=link[name="Help me choose"].or_(self.page.text=Help me choose)

    @property
    def Purifier filters(self):
        """Link to purifier filters."""
        return self.page.role=link[name="Purifier filters"].or_(self.page.text=Purifier filters)

    @property
    def Exclusive Offer Close Button(self):
        """Button to close the exclusive offer banner."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label="Close"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The 'Air purifier' link is visible
        await The 'Search products and parts' search box is visible
        await The 'Air Purifiers' link is visible
        await The 'Exclusive: 10X reward points' banner is visible