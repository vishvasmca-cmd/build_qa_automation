from playwright.async_api import Page, expect

class HomePage:
    """
    The Dyson India homepage showcases various Dyson products and provides navigation to different product categories, support, and company information. The primary purpose is to promote Dyson products and facilitate online shopping.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Dyson company logo, navigates to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.img[alt='Dyson'])

    @property
    def search_products(self):
        """Search input field for products and parts."""
        return self.page.css=button[aria-label='Open search'].or_(self.page.input[placeholder='Search products and parts'])

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
    def shop_now_button(self):
        """Button to shop now."""
        return self.page.text=Shop now.or_(self.page.a[aria-label='Shop now'])

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

    @property
    def cart_icon(self):
        """Link to the shopping cart."""
        return self.page.css=a[aria-label='Basket'].or_(self.page.svg[data-test='mini-basket-icon'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title of the page is 'Dyson India | Official Website'
        await The Dyson logo is visible
        await The 'Search products and parts' search box is present
        await The 'Shop now' button is visible
        await The main hero section text 'Compact. Powerful. Yet quiet.' is visible