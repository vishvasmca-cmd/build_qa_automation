from playwright.async_api import Page, expect

class DysonV15DetectVacuumCleanerPage:
    """
    This page is the homepage for Dyson India, showcasing various products and promotions.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=search.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=a[aria-label='Shop now'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners category page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/offers'])

    @property
    def hair_care(self):
        """Link to the hair care products page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care'])

    @property
    def air_purifier(self):
        """Link to the air purifier products page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-purifiers'])

    @property
    def headphones(self):
        """Link to the headphones products page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting(self):
        """Link to the lighting products page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/lighting'])

    @property
    def support(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/support'])

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'