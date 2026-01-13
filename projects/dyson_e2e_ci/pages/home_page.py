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
        return self.page.//a[@aria-label='Dyson'].or_(self.page.css=a.header__logo-link)

    @property
    def search_products_and_parts(self):
        """Search input box to find products and parts."""
        return self.page.css=input[placeholder='Search products and parts'].or_(self.page.//input[@placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the product page."""
        return self.page.//a[text()='Shop now'].or_(self.page.css=a[aria-label='Shop now'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the Vacuum & wet cleaners product category."""
        return self.page.//a[text()='Vacuum & wet cleaners'].or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def air_purifier(self):
        """Link to the Air purifier product category."""
        return self.page.//a[text()='Air purifier'].or_(self.page.css=a[href='/air-treatment'])

    @property
    def headphones(self):
        """Link to the Headphones product category."""
        return self.page.//a[text()='Headphones'].or_(self.page.css=a[href='/headphones'])

    @property
    def lighting(self):
        """Link to the Lighting product category."""
        return self.page.//a[text()='Lighting'].or_(self.page.css=a[href='/lighting'])

    @property
    def support(self):
        """Link to the Support page."""
        return self.page.//a[text()='Support'].or_(self.page.css=a[href='/support'])

    @property
    def best_sellers(self):
        """Link to the Best sellers page."""
        return self.page.//a[text()='Best sellers'].or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The Dyson logo is visible
        await The 'Search products and parts' search box is present
        await The 'Shop now' button is visible
        await The 'Vacuum & wet cleaners' link is visible
        await The 'Air purifier' link is visible
        await The 'Headphones' link is visible
        await The 'Lighting' link is visible
        await The 'Support' link is visible
        await The 'Best sellers' link is visible