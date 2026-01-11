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
        """Dyson logo that navigates to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.css=svg[class*='DysonLogo'])

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.css=input[placeholder='Search products and parts'].or_(self.page.//input[@placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the product page."""
        return self.page.//a[contains(text(),'Shop now')].or_(self.page.css=a[class*='Button'][href*='/products/'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.//a[text()='Deals'].or_(self.page.css=a[href*='/deals'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.//a[text()='Vacuum & wet cleaners'].or_(self.page.css=a[href*='/vacuums'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier page."""
        return self.page.//a[text()='Air purifier'].or_(self.page.css=a[href*='/air-treatment'])

    @property
    def headphones_link(self):
        """Link to the headphones page."""
        return self.page.//a[text()='Headphones'].or_(self.page.css=a[href*='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting page."""
        return self.page.//a[text()='Lighting'].or_(self.page.css=a[href*='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.//a[text()='Support'].or_(self.page.css=a[href*='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.//a[text()='Best sellers'].or_(self.page.css=a[href*='/best-sellers'])

    @property
    def cart_icon(self):
        """Icon to navigate to the shopping cart."""
        return self.page.css=a[aria-label='Basket'].or_(self.page.//a[@aria-label='Basket'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Dyson logo is visible
        await Search input field is present
        await At least one product category link is visible (e.g., 'Vacuum & wet cleaners')
        await The 'Shop now' button is visible