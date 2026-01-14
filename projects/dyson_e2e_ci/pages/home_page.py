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
        """Dyson logo that navigates to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.css=svg[class*='DysonLogo'])

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the shop page for the featured product."""
        return self.page.//a[text()='Shop now'].or_(self.page.css=a[class*='Button'][href*='/shop'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.//a[text()='Deals'].or_(self.page.css=a[href*='/deals'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.//a[text()='Vacuum & wet cleaners'].or_(self.page.css=a[href*='/vacuums'])

    @property
    def hair_care_link(self):
        """Link to the hair care products page."""
        return self.page.//a[text()='Hair care'].or_(self.page.css=a[href*='/hair-care'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier products page."""
        return self.page.//a[text()='Air purifier'].or_(self.page.css=a[href*='/air-treatment'])

    @property
    def headphones_link(self):
        """Link to the headphones products page."""
        return self.page.//a[text()='Headphones'].or_(self.page.css=a[href*='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting products page."""
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
    def discover_dyson_link(self):
        """Link to the Discover Dyson page."""
        return self.page.//a[text()='Discover Dyson'].or_(self.page.css=a[href*='/dyson-technology'])

    @property
    def for_business_link(self):
        """Link to the For business page."""
        return self.page.//a[text()='For business'].or_(self.page.css=a[href*='/for-business'])

    @property
    def store_finder_link(self):
        """Link to the Store finder page."""
        return self.page.//a[text()='Store finder'].or_(self.page.css=a[href*='/store-finder'])

    @property
    def register_machine_link(self):
        """Link to the Register machine page."""
        return self.page.//a[text()='Register machine'].or_(self.page.css=a[href*='/register'])

    @property
    def contact_us_link(self):
        """Link to the Contact us page."""
        return self.page.//a[text()='Contact us'].or_(self.page.css=a[href*='/contact'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'