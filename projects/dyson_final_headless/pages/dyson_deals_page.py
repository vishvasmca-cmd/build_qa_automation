from playwright.async_api import Page, expect

class DysonDealsPage:
    """
    This page displays Dyson deals and promotions, allowing users to browse and purchase discounted products.
    URL Pattern: https://www.dyson.in/deals
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Products and Parts(self):
        """Search input field to find specific products or parts."""
        return self.page.aria/Search products and parts.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Deals Link(self):
        """Link to the main deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def Vacuum & wet cleaners Link(self):
        """Link to the vacuum and wet cleaners category."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def Cord-free Vacuums Link(self):
        """Link to the cord-free vacuums category."""
        return self.page.text=Cord-free Vacuums.or_(self.page.css=a[href='/cordless-vacuums'])

    @property
    def Corded vacuums Link(self):
        """Link to the corded vacuums category."""
        return self.page.text=Corded vacuums.or_(self.page.css=a[href='/corded-vacuums'])

    @property
    def Wet & Dry vacuum cleaners Link(self):
        """Link to the wet and dry vacuum cleaners category."""
        return self.page.text=Wet & Dry vacuum cleaners.or_(self.page.css=a[href='/wet-and-dry-vacuums'])

    @property
    def Cart Icon(self):
        """Button to view the shopping cart."""
        return self.page.aria/View Basket.or_(self.page.css=button[aria-label='View Basket'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Deals and Offers | Dyson'
        await The 'Deals' link is visible.
        await The 'Search products and parts' search box is visible.