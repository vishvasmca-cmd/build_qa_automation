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
        """Navigates to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.css=a[aria-label='Homepage'])

    @property
    def search_products_and_parts(self):
        """Search input box to find products and parts."""
        return self.page.xpath=//input[@placeholder='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the shop page."""
        return self.page.xpath=//a[text()='Shop now'].or_(self.page.css=a[class*='button'][href*='/shop'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href*='/deals'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href*='/vacuum-cleaners'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href*='/air-purifiers'])

    @property
    def headphones_link(self):
        """Link to the headphones page."""
        return self.page.text=Headphones.or_(self.page.css=a[href*='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting page."""
        return self.page.text=Lighting.or_(self.page.css=a[href*='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href*='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href*='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'