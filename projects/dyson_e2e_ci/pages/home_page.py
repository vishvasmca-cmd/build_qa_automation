from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products, particularly the 'hushjet Purifier Compact', and provide navigation to different product categories and information.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the product page for the featured 'hushjet Purifier Compact'."""
        return self.page.text=Shop now.or_(self.page.css=a[href*='/purifiers/hushjet'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners product category."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href*='/vacuum-cleaners'])

    @property
    def air_purifier(self):
        """Link to the air purifier product category."""
        return self.page.text=Air purifier.or_(self.page.css=a[href*='/air-purifiers'])

    @property
    def headphones(self):
        """Link to the headphones product category."""
        return self.page.text=Headphones.or_(self.page.css=a[href*='/headphones'])

    @property
    def lighting(self):
        """Link to the lighting product category."""
        return self.page.text=Lighting.or_(self.page.css=a[href*='/lighting'])

    @property
    def support(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href*='/support'])

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href*='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson India'
        await Header text 'Compact. Powerful. Yet quiet.' is visible
        await The 'Search products and parts' search box is present
        await The 'Shop now' button is present