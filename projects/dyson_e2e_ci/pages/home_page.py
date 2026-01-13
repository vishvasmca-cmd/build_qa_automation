from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. It showcases products, deals, and provides navigation to different sections of the website.
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
        """Search input box to find products and parts."""
        return self.page.css=input[placeholder='Search products and parts'].or_(self.page.//input[@placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the Hushjet purifier product page."""
        return self.page.//a[contains(text(),'Shop now')].or_(self.page.css=a[class*='Button'][href*='/purifiers/hushjet'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.//a[text()='Deals'].or_(self.page.css=a[href='/deals'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.//a[text()='Vacuum & wet cleaners'].or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def hair_care_link(self):
        """Link to the hair care products page."""
        return self.page.//a[text()='Hair care'].or_(self.page.css=a[href='/hair-care'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier products page."""
        return self.page.//a[text()='Air purifier'].or_(self.page.css=a[href='/air-treatment'])

    @property
    def headphones_link(self):
        """Link to the headphones products page."""
        return self.page.//a[text()='Headphones'].or_(self.page.css=a[href='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting products page."""
        return self.page.//a[text()='Lighting'].or_(self.page.css=a[href='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.//a[text()='Support'].or_(self.page.css=a[href='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.//a[text()='Best sellers'].or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The Dyson logo is visible
        await The search input box is visible
        await The 'Shop now' button is visible
        await The 'Dyson.in exclusive: 24 months no cost EMI' banner is visible