from playwright.async_api import Page, expect

class DysonIndiaOfficialWebsitePage:
    """
    This page is a landing page for the Dyson Hushjet Purifier Compact. The primary purpose is to showcase the product and encourage users to purchase it.
    URL Pattern: https://www.dyson.in/airwrap-origin-nickel-copper
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field in the header."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=.button.button--primary)

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def hair_care(self):
        """Link to the hair care page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care'])

    @property
    def air_purifier(self):
        """Link to the air purifier page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-treatment'])

    @property
    def headphones(self):
        """Link to the headphones page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting(self):
        """Link to the lighting page."""
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
        await Page title contains 'Dyson'
        await Header text 'Compact. Powerful. Yet quiet.' is visible
        await The 'Shop now' button is visible