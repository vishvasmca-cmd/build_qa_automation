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
        """Link to the Dyson homepage."""
        return self.page.//a[@aria-label='Dyson'].or_(self.page.a[href='/'])

    @property
    def search_products_and_parts(self):
        """Search input field for products and parts."""
        return self.page.xpath=//input[@placeholder='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to shop for the featured product."""
        return self.page.text=Shop now.or_(self.page.css=a[aria-label='Shop now'])

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
        await Page title contains 'Dyson'
        await The Dyson logo is visible
        await The search input field is present
        await The 'Shop now' button is visible
        await The 'Vacuum & wet cleaners' link is present