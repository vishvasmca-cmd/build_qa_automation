from playwright.async_api import Page, expect

class DysonAirTreatmentPage:
    """
    This page is the Dyson India Headphones landing page, showcasing Dyson's headphone products and related information.
    URL Pattern: https://www.dyson.in/headphones
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input box to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def headphones_link(self):
        """Link to the Headphones product category page."""
        return self.page.text=Headphones.or_(self.page.css=a[href*='headphones'])

    @property
    def deals_link(self):
        """Link to the Deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href*='deals'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the Vacuum & wet cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href*='vacuum-cleaners'])

    @property
    def air_purifier_link(self):
        """Link to the Air purifier page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href*='air-purifiers'])

    @property
    def lighting_link(self):
        """Link to the Lighting page."""
        return self.page.text=Lighting.or_(self.page.css=a[href*='lighting'])

    @property
    def support_link(self):
        """Link to the Support page."""
        return self.page.text=Support.or_(self.page.css=a[href*='support'])

    @property
    def best_sellers_link(self):
        """Link to the Best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href*='best-sellers'])

    @property
    def close_reward_points_banner(self):
        """Button to close the reward points banner."""
        return self.page.text=X.or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Page contains the text 'Dyson.in exclusive: Pay in up to 24 monthly instalments with 0% interest#'
        await The 'Headphones' link is visible