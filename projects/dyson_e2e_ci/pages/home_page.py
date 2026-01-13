from playwright.async_api import Page, expect

class HomePage:
    """
    The Dyson India homepage showcasing products and promotions.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Dyson logo in the top left corner."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.css=svg[class*='DysonLogo'])

    @property
    def search_products_and_parts(self):
        """Search input box to find products and parts."""
        return self.page.css=input[placeholder='Search products and parts'].or_(self.page.css=div[class*='search'])

    @property
    def shop_now(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=a[class*='Button'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners category."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def air_purifier(self):
        """Link to the air purifier category."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-treatment'])

    @property
    def headphones(self):
        """Link to the headphones category."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting(self):
        """Link to the lighting category."""
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