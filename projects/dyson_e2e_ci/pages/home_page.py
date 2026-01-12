from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products and provide navigation to different product categories and information.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Link to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.css=svg[class*='DysonLogo'])

    @property
    def search_products_and_parts(self):
        """Button to open the search functionality."""
        return self.page.css=button[aria-label='Search products and parts'].or_(self.page.text=Search products and parts)

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href*='/deals'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href*='/vacuum-cleaners'])

    @property
    def hair_care(self):
        """Link to the hair care products page."""
        return self.page.text=Hair care.or_(self.page.css=a[href*='/hair-care'])

    @property
    def air_purifier(self):
        """Link to the air purifier products page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href*='/air-purifiers'])

    @property
    def headphones(self):
        """Link to the headphones products page."""
        return self.page.text=Headphones.or_(self.page.css=a[href*='/headphones'])

    @property
    def lighting(self):
        """Link to the lighting products page."""
        return self.page.text=Lighting.or_(self.page.css=a[href*='/lighting'])

    @property
    def support(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href*='/support'])

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href*='/best-sellers'])

    @property
    def shop_now(self):
        """Button to shop the featured product."""
        return self.page.text=Shop now.or_(self.page.css=a[class*='Button'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson India'
        await Page contains the Dyson logo
        await Page contains the 'Search products and parts' button
        await Page contains the 'Deals' link
        await Page contains the 'Vacuum & wet cleaners' link
        await Page contains the 'Hair care' link
        await Page contains the 'Air purifier' link