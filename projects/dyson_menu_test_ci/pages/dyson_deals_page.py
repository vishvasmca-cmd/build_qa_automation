from playwright.async_api import Page, expect

class DysonDealsPage:
    """
    This page displays Dyson deals and promotions, allowing users to browse and purchase discounted products.
    URL Pattern: https://www.dyson.in/deals
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Deals Link(self):
        """Link to the deals page."""
        return self.page.role=link[name="Deals"].or_(self.page.text=Deals)

    @property
    def Vacuum & wet cleaners Link(self):
        """Link to the vacuum and wet cleaners category."""
        return self.page.role=link[name="Vacuum & wet cleaners"].or_(self.page.text=Vacuum & wet cleaners)

    @property
    def Search products and parts(self):
        """Search input field."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Cord-free Vacuums Link(self):
        """Link to Cord-free Vacuums."""
        return self.page.role=link[name="Cord-free Vacuums"].or_(self.page.text=Cord-free Vacuums)

    @property
    def Corded vacuums Link(self):
        """Link to Corded vacuums."""
        return self.page.role=link[name="Corded vacuums"].or_(self.page.text=Corded vacuums)

    @property
    def Wet & Dry vacuum cleaners Link(self):
        """Link to Wet & Dry vacuum cleaners."""
        return self.page.role=link[name="Wet & Dry vacuum cleaners"].or_(self.page.text=Wet & Dry vacuum cleaners)

    @property
    def Wet floor cleaners Link(self):
        """Link to Wet floor cleaners."""
        return self.page.role=link[name="Wet floor cleaners"].or_(self.page.text=Wet floor cleaners)

    @property
    def Shop all vacuum cleaners Link(self):
        """Link to Shop all vacuum cleaners."""
        return self.page.role=link[name="Shop all vacuum cleaners"].or_(self.page.text=Shop all vacuum cleaners)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Deals'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'
        await Page contains the text 'Shop by category'