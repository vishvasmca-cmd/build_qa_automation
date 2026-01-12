from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products, particularly the Hushjet Purifier Compact, and provide navigation to different product categories and information.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Link to the Dyson homepage."""
        return self.page.//a[@aria-label='Dyson'].or_(self.page.img[alt='Dyson'])

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.css=button[aria-label='Search products and parts'].or_(self.page.text=Search products and parts)

    @property
    def shop_now_hushjet_(self):
        """Button to navigate to the Hushjet Purifier Compact product page."""
        return self.page.text=Shop now.or_(self.page.css=.button--link)

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.a[href='/deals.html'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.a[href='/vacuum-cleaners.html'])

    @property
    def air_purifier(self):
        """Link to the air purifier page."""
        return self.page.text=Air purifier.or_(self.page.a[href='/air-treatment.html'])

    @property
    def headphones(self):
        """Link to the headphones page."""
        return self.page.text=Headphones.or_(self.page.a[href='/headphones.html'])

    @property
    def lighting(self):
        """Link to the lighting page."""
        return self.page.text=Lighting.or_(self.page.a[href='/lighting.html'])

    @property
    def support(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.a[href='/support.html'])

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.a[href='/best-sellers.html'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The 'Dyson Logo' is visible
        await The 'Search products and parts' search box is visible
        await The 'Shop now' button is visible
        await The text 'Compact. Powerful. Yet quiet.' is visible