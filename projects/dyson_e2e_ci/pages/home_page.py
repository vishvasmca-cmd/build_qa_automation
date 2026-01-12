from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. It showcases products and provides navigation to different sections of the website.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Dyson logo that navigates to the homepage."""
        return self.page.role=link[name='Homepage'].or_(self.page.css=a[aria-label='Homepage'])

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox[name='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/en-IN/purifiers/compact'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners section."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/en-IN/vacuum-cleaners'])

    @property
    def air_purifier(self):
        """Link to the air purifier section."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/en-IN/air-treatment'])

    @property
    def headphones(self):
        """Link to the headphones section."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/en-IN/headphones'])

    @property
    def lighting(self):
        """Link to the lighting section."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/en-IN/lighting'])

    @property
    def support(self):
        """Link to the support section."""
        return self.page.text=Support.or_(self.page.css=a[href='/en-IN/support'])

    @property
    def best_sellers(self):
        """Link to the best sellers section."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/en-IN/deals'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson India'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'