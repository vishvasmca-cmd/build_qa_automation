from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products and provide navigation to different product categories and information.
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
        """Button to navigate to the Hushjet Purifier Compact product page."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/air-treatment/purifiers/hushjet/hushjet-purifier-compact-nickel-iron'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners product category page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier product category page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-treatment'])

    @property
    def headphones_link(self):
        """Link to the headphones product category page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting product category page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/shop/offers'])

    @property
    def discover_dyson_link(self):
        """Link to the Discover Dyson page."""
        return self.page.text=Discover Dyson.or_(self.page.css=a[href='/dyson-technology'])

    @property
    def for_business_link(self):
        """Link to the For Business page."""
        return self.page.text=For business.or_(self.page.css=a[href='/for-business'])

    @property
    def store_finder_link(self):
        """Link to the Store Finder page."""
        return self.page.text=Store finder.or_(self.page.css=a[href='/store-finder'])

    @property
    def register_machine_link(self):
        """Link to the Register Machine page."""
        return self.page.text=Register machine.or_(self.page.css=a[href='/register'])

    @property
    def contact_us_link(self):
        """Link to the Contact Us page."""
        return self.page.text=Contact us.or_(self.page.css=a[href='/support/contact-us'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title of the page is 'Dyson India | Official Website'
        await The 'Dyson' logo is visible.
        await The main hero section text 'Compact. Powerful. Yet quiet.' is visible.
        await The 'Shop now' button is visible.