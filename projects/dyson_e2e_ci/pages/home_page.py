from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage of Dyson India, showcasing their products and promotions.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products(self):
        """Search input field for products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the product page featured in the hero section."""
        return self.page.text=Shop now.or_(self.page.css=.button.button--primary)

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def air_purifier(self):
        """Link to the air purifiers page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-purifiers'])

    @property
    def headphones(self):
        """Link to the headphones page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting(self):
        """Link to the lighting page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/lighting'])

    @property
    def support(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/support'])

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers'])

    @property
    def cart(self):
        """Link to the shopping cart."""
        return self.page.role=img[name='Basket'].or_(self.page.css=a[aria-label='Basket'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Presence of the Dyson logo
        await Presence of the 'Search products and parts' search box
        await Presence of the 'Shop now' button
        await Presence of the 'Dyson.in exclusive: 24 months no cost EMI' banner