from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. It showcases products and provides navigation to different sections of the website.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Dyson logo that navigates to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.img[alt='Dyson'])

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.css=button[aria-label='Search'].or_(self.page.css=div.search-input > input)

    @property
    def shop_now_button(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=a.button.button--primary)

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.a[href='/deals'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.a[href='/vacuum-cleaners'])

    @property
    def hair_care_link(self):
        """Link to the hair care products page."""
        return self.page.text=Hair care.or_(self.page.a[href='/hair-care'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier products page."""
        return self.page.text=Air purifier.or_(self.page.a[href='/air-treatment'])

    @property
    def headphones_link(self):
        """Link to the headphones products page."""
        return self.page.text=Headphones.or_(self.page.a[href='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting products page."""
        return self.page.text=Lighting.or_(self.page.a[href='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.a[href='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.a[href='/best-sellers'])

    @property
    def discover_dyson_link(self):
        """Link to the Discover Dyson page."""
        return self.page.text=Discover Dyson.or_(self.page.a[href='/dyson-technology'])

    @property
    def for_business_link(self):
        """Link to the For business page."""
        return self.page.text=For business.or_(self.page.a[href='/for-business'])

    @property
    def store_finder_link(self):
        """Link to the Store finder page."""
        return self.page.text=Store finder.or_(self.page.a[href='/store-finder'])

    @property
    def register_machine_link(self):
        """Link to the Register machine page."""
        return self.page.text=Register machine.or_(self.page.a[href='/register'])

    @property
    def contact_us_link(self):
        """Link to the Contact us page."""
        return self.page.text=Contact us.or_(self.page.a[href='/support/contact-us'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The Dyson logo is displayed
        await The 'Search products and parts' search box is displayed
        await The 'Shop now' button is displayed
        await The 'Dyson.in exclusive: 24 months no cost EMI' banner is displayed