from playwright.async_api import Page, expect

class DysonIndiaPage:
    """
    This is the homepage of Dyson India. It showcases various Dyson products and provides navigation to different product categories and support resources.
    URL Pattern: https://www.dyson.in/*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the product details page."""
        return self.page.text=Shop now.or_(self.page.css=.button.button--primary)

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
        await Page title contains 'Dyson'
        await Header text contains 'Compact. Powerful. Yet quiet.'
        await The 'Shop now' button is visible