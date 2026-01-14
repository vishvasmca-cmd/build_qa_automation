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
        return self.page.text=Shop now.or_(self.page.css=a[href='/purifiers/compact'])

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
    def deals_link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def hair_care_link(self):
        """Link to the hair care product category page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care'])

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
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title of the page contains 'Dyson'
        await The main hero section with 'hushjet Purifier Compact' is displayed
        await The 'Search products and parts' search box is present
        await The Dyson logo is visible