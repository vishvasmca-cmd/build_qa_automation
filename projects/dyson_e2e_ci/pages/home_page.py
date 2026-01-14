from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products and provide navigation to different product categories and support resources.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input box to find products and parts."""
        return self.page.aria/Search products and parts.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the Hushjet purifier product page."""
        return self.page.text/Shop now.or_(self.page.css=a[href='/en-IN/purifiers/compact'])

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text/Deals.or_(self.page.css=a[href='/en-IN/deals'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.text/Vacuum & wet cleaners.or_(self.page.css=a[href='/en-IN/vacuum-cleaners'])

    @property
    def hair_care(self):
        """Link to the hair care products page."""
        return self.page.text/Hair care.or_(self.page.css=a[href='/en-IN/hair-care'])

    @property
    def air_purifier(self):
        """Link to the air purifier products page."""
        return self.page.text/Air purifier.or_(self.page.css=a[href='/en-IN/air-treatment'])

    @property
    def headphones(self):
        """Link to the headphones products page."""
        return self.page.text/Headphones.or_(self.page.css=a[href='/en-IN/headphones'])

    @property
    def lighting(self):
        """Link to the lighting products page."""
        return self.page.text/Lighting.or_(self.page.css=a[href='/en-IN/lighting'])

    @property
    def support(self):
        """Link to the support page."""
        return self.page.text/Support.or_(self.page.css=a[href='/en-IN/support'])

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.text/Best sellers.or_(self.page.css=a[href='/en-IN/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The Dyson logo is visible
        await The 'Search products and parts' search box is present
        await The 'Shop now' button is visible
        await The text 'Compact. Powerful. Yet quiet.' is visible