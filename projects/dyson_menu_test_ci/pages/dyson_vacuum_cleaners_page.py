from playwright.async_api import Page, expect

class DysonVacuumCleanersPage:
    """
    This page is the Dyson Vacuum & Wet Cleaners landing page, showcasing different types of vacuum cleaners.
    URL Pattern: https://www.dyson.in/hair-care
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def vacuum_wet_cleaners_tab(self):
        """Link to the Vacuum & wet cleaners section."""
        return self.page.role=link[name="Vacuum & wet cleaners"].or_(self.page.text=Vacuum & wet cleaners)

    @property
    def search_products_and_parts(self):
        """Search input box to find products and parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

    @property
    def cord_free_vacuums(self):
        """Link to Cord-free Vacuums section."""
        return self.page.role=link[name="Cord-free Vacuums"].or_(self.page.text=Cord-free Vacuums)

    @property
    def corded_vacuums(self):
        """Link to Corded vacuums section."""
        return self.page.role=link[name="Corded vacuums"].or_(self.page.text=Corded vacuums)

    @property
    def wet_dry_vacuum_cleaners(self):
        """Link to Wet & Dry vacuum cleaners section."""
        return self.page.role=link[name="Wet & Dry vacuum cleaners"].or_(self.page.text=Wet & Dry vacuum cleaners)

    @property
    def wet_floor_cleaners(self):
        """Link to Wet floor cleaners section."""
        return self.page.role=link[name="Wet floor cleaners"].or_(self.page.text=Wet floor cleaners)

    @property
    def shop_all_vacuum_cleaners(self):
        """Link to Shop all vacuum cleaners section."""
        return self.page.role=link[name="Shop all vacuum cleaners"].or_(self.page.text=Shop all vacuum cleaners)

    @property
    def help_me_choose(self):
        """Button to help me choose a vacuum cleaner."""
        return self.page.role=button[name="Help me choose"].or_(self.page.text=Help me choose)

    @property
    def close_exclusive_offer(self):
        """Button to close the exclusive offer."""
        return self.page.role=button[name="Close"].or_(self.page.css=button[aria-label="Close"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Vacuum & wet cleaners'
        await Page contains the heading 'Vacuums & wet cleaners'
        await The 'Search products and parts' search box is present
        await The 'Help me choose' button is present