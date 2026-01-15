from playwright.async_api import Page, expect

class DysonWashg1WetFloorCleanerPage:
    """
    This page is the homepage for Dyson India, showcasing various products and promotions.
    URL Pattern: https://www.dyson.in/*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the shop."""
        return self.page.text=Shop now.or_(self.page.css=.button.button--green)

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/offers'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier page."""
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
    def discover_dyson_link(self):
        """Link to the Discover Dyson page."""
        return self.page.text=Discover Dyson.or_(self.page.css=a[href='/dyson-technology'])

    @property
    def for_business_link(self):
        """Link to the For business page."""
        return self.page.text=For business.or_(self.page.css=a[href='/for-business'])

    @property
    def store_finder_link(self):
        """Link to the Store finder page."""
        return self.page.text=Store finder.or_(self.page.css=a[href='/store-finder'])

    @property
    def register_machine_link(self):
        """Link to the Register machine page."""
        return self.page.text=Register machine.or_(self.page.css=a[href='/register'])

    @property
    def contact_us_link(self):
        """Link to the Contact us page."""
        return self.page.text=Contact us.or_(self.page.css=a[href='/support/contact-us'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header text contains 'This wedding season, the difference is Dyson'
        await Element with text 'Shop now' is visible