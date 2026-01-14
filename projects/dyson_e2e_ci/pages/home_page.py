from playwright.async_api import Page, expect

class HomePage:
    """
    The Dyson India homepage is designed to showcase Dyson products, provide information about deals and offers, and facilitate navigation to different product categories and support resources.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the product page for the featured air purifier."""
        return self.page.text=Shop now.or_(self.page.css=a[href*='/air-purifiers/dyson-purifier-compact'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def vacuum_and_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def air_purifier_link(self):
        """Link to the air purifiers page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-purifiers'])

    @property
    def headphones_link(self):
        """Link to the headphones page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers'])

    @property
    def cart_icon(self):
        """Link to the shopping cart."""
        return self.page.css=a[aria-label='Basket'].or_(self.page.css=a[href='/cart'])

    @property
    def close_promotion_modal(self):
        """Button to close the promotion modal."""
        return self.page.css=button[aria-label='Close'].or_(self.page.text=Close)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header text contains 'Compact. Powerful. Yet quiet.'
        await The Dyson logo is visible
        await The 'Search products and parts' search box is present