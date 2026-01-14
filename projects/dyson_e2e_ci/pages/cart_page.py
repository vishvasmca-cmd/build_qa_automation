from playwright.async_api import Page, expect

class CartPage:
    """
    This is the homepage of the Dyson India website, showcasing featured deals and products.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.role=link[name='Deals'].or_(self.page.text=Deals)

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum and wet cleaners page."""
        return self.page.role=link[name='Vacuum & wet cleaners'].or_(self.page.text=Vacuum & wet cleaners)

    @property
    def hair_care_link(self):
        """Link to the hair care products page."""
        return self.page.role=link[name='Hair care'].or_(self.page.text=Hair care)

    @property
    def air_purifier_link(self):
        """Link to the air purifier products page."""
        return self.page.role=link[name='Air purifier'].or_(self.page.text=Air purifier)

    @property
    def headphones_link(self):
        """Link to the headphones products page."""
        return self.page.role=link[name='Headphones'].or_(self.page.text=Headphones)

    @property
    def lighting_link(self):
        """Link to the lighting products page."""
        return self.page.role=link[name='Lighting'].or_(self.page.text=Lighting)

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.role=link[name='Support'].or_(self.page.text=Support)

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.role=link[name='Best sellers'].or_(self.page.text=Best sellers)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title contains 'Dyson India'
        await Verify the presence of the Dyson logo
        await Verify the presence of 'Featured deals' heading