from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products and promotions.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Link to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.css=a[aria-label='Homepage'])

    @property
    def search_products_and_parts(self):
        """Button to open the search functionality."""
        return self.page.css=button[aria-label='Search products and parts'].or_(self.page.text=Search products and parts)

    @property
    def shop_now(self):
        """Link to the hair care products page."""
        return self.page.text=Shop now.or_(self.page.css=a[href*='/hair-care'])

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def hair_care(self):
        """Link to the hair care page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care'])

    @property
    def air_purifier(self):
        """Link to the air purifier page."""
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
    def discover_dyson(self):
        """Link to the Discover Dyson page."""
        return self.page.text=Discover Dyson.or_(self.page.css=a[href='/discover-dyson'])

    @property
    def for_business(self):
        """Link to the For business page."""
        return self.page.text=For business.or_(self.page.css=a[href='/for-business'])

    @property
    def store_finder(self):
        """Link to the Store finder page."""
        return self.page.text=Store finder.or_(self.page.css=a[href='/store-finder'])

    @property
    def register_machine(self):
        """Link to the Register machine page."""
        return self.page.text=Register machine.or_(self.page.css=a[href='/register-machine'])

    @property
    def contact_us(self):
        """Link to the Contact us page."""
        return self.page.text=Contact us.or_(self.page.css=a[href='/contact-us'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Page contains the text 'This wedding season, the difference is Dyson'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'