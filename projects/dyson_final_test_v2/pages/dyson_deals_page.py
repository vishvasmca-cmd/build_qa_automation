from playwright.async_api import Page, expect

class DysonDealsPage:
    """
    This page displays deals and promotions offered by Dyson India. It allows users to browse and explore various product categories and specific deals.
    URL Pattern: https://www.dyson.in/deals
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Deals Link(self):
        """Link to the deals page."""
        return self.page.role=link[name='Deals'].or_(self.page.text=Deals)

    @property
    def Vacuum & wet cleaners Link(self):
        """Link to the vacuum and wet cleaners page."""
        return self.page.role=link[name='Vacuum & wet cleaners'].or_(self.page.text=Vacuum & wet cleaners)

    @property
    def Search Products and Parts(self):
        """Search input box to find products and parts."""
        return self.page.role=searchbox[name='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Cord-free Vacuums Link(self):
        """Link to Cord-free Vacuums page."""
        return self.page.role=link[name='Cord-free Vacuums'].or_(self.page.text=Cord-free Vacuums)

    @property
    def Corded Vacuums Link(self):
        """Link to Corded Vacuums page."""
        return self.page.role=link[name='Corded vacuums'].or_(self.page.text=Corded vacuums)

    @property
    def Wet & Dry vacuum cleaners Link(self):
        """Link to Wet & Dry vacuum cleaners page."""
        return self.page.role=link[name='Wet & Dry vacuum cleaners'].or_(self.page.text=Wet & Dry vacuum cleaners)

    @property
    def Wet floor cleaners Link(self):
        """Link to Wet floor cleaners page."""
        return self.page.role=link[name='Wet floor cleaners'].or_(self.page.text=Wet floor cleaners)

    @property
    def Shop all vacuum cleaners Link(self):
        """Link to Shop all vacuum cleaners page."""
        return self.page.role=link[name='Shop all vacuum cleaners'].or_(self.page.text=Shop all vacuum cleaners)

    @property
    def Help me choose Link(self):
        """Link to Help me choose page."""
        return self.page.role=link[name='Help me choose'].or_(self.page.text=Help me choose)

    @property
    def Stands, tools, batteries & filters Link(self):
        """Link to Stands, tools, batteries & filters page."""
        return self.page.role=link[name='Stands, tools, batteries & filters'].or_(self.page.text=Stands, tools, batteries & filters)

    @property
    def Dyson Dust Research Link(self):
        """Link to Dyson Dust Research page."""
        return self.page.role=link[name='Dyson Dust Research'].or_(self.page.text=Dyson Dust Research)

    @property
    def Pet Science Link(self):
        """Link to Pet Science page."""
        return self.page.role=link[name='Pet Science'].or_(self.page.text=Pet Science)

    @property
    def Close Exclusive Offer(self):
        """Button to close the exclusive offer popup."""
        return self.page.role=button[name='Close'].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Deals | Dyson India'
        await Header text contains 'Shop by category'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'