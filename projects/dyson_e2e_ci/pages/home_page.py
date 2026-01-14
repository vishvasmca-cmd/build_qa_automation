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
    def shop_now(self):
        """Button to navigate to the product page for the featured air purifier."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/en-IN/purifiers/compact'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners product category."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/en-IN/vacuum-cleaners'])

    @property
    def air_purifier(self):
        """Link to the air purifier product category."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/en-IN/air-treatment'])

    @property
    def headphones(self):
        """Link to the headphones product category."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/en-IN/headphones'])

    @property
    def lighting(self):
        """Link to the lighting product category."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/en-IN/lighting'])

    @property
    def support(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/en-IN/support'])

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/en-IN/best-sellers'])

    @property
    def discover_dyson(self):
        """Link to the Discover Dyson page."""
        return self.page.text=Discover Dyson.or_(self.page.css=a[href='/en-IN/dyson-technology'])

    @property
    def for_business(self):
        """Link to the For business page."""
        return self.page.text=For business.or_(self.page.css=a[href='/en-IN/for-business'])

    @property
    def store_finder(self):
        """Link to the Store finder page."""
        return self.page.text=Store finder.or_(self.page.css=a[href='/en-IN/store-finder'])

    @property
    def register_machine(self):
        """Link to the Register machine page."""
        return self.page.text=Register machine.or_(self.page.css=a[href='/en-IN/support/your-dyson/registration'])

    @property
    def contact_us(self):
        """Link to the Contact us page."""
        return self.page.text=Contact us.or_(self.page.css=a[href='/en-IN/support/contact-us'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'