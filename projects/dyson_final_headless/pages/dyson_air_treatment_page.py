from playwright.async_api import Page, expect

class DysonAirTreatmentPage:
    """
    This page is the Dyson Air Treatment landing page, specifically focusing on Air Purifiers. It allows users to explore and learn about Dyson's air purifier products.
    URL Pattern: https://www.dyson.in/headphones
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
        """Link to view all Air Purifiers."""
        return self.page.role=link[name="Air Purifiers"].or_(self.page.text=Air Purifiers)

    @property
    def Purifier + Heaters(self):
        """Link to view Purifier + Heaters."""
        return self.page.role=link[name="Purifier + Heaters"].or_(self.page.text=Purifier + Heaters)

    @property
    def Shop all air purifiers(self):
        """Link to view all air purifiers."""
        return self.page.role=link[name="Shop all air purifiers"].or_(self.page.text=Shop all air purifiers)

    @property
    def Help me choose(self):
        """Link to Help me choose."""
        return self.page.role=link[name="Help me choose"].or_(self.page.text=Help me choose)

    @property
    def Purifier filters(self):
        """Link to Purifier filters."""
        return self.page.role=link[name="Purifier filters"].or_(self.page.text=Purifier filters)

    @property
    def Dyson air quality backpack research(self):
        """Link to Dyson air quality backpack research."""
        return self.page.role=link[name="Dyson air quality backpack research"].or_(self.page.text=Dyson air quality backpack research)

    @property
    def Dyson Purifier Filter Research(self):
        """Link to Dyson Purifier Filter Research."""
        return self.page.role=link[name="Dyson Purifier Filter Research"].or_(self.page.text=Dyson Purifier Filter Research)

    @property
    def Dyson Purifier Testing Standards(self):
        """Link to Dyson Purifier Testing Standards."""
        return self.page.role=link[name="Dyson Purifier Testing Standards"].or_(self.page.text=Dyson Purifier Testing Standards)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title contains 'Dyson'
        await Verify the 'Air purifier' link is visible in the navigation bar
        await Verify the 'Search products and parts' search box is present
        await Verify the 'Air Purifiers' link is visible under 'Explore air purifier'
        await Verify the 'Purifier + Heaters' link is visible under 'Explore air purifier'
        await Verify the 'Shop all air purifiers' link is visible under 'Explore air purifier'