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
        """Link to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.css=a[aria-label='Homepage'])

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.xpath=//input[@placeholder='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the Hushjet purifier product page."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/en-IN/purifiers/hushjet'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners product category."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/en-IN/vacuum-cleaners'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier product category."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/en-IN/air-treatment'])

    @property
    def headphones_link(self):
        """Link to the headphones product category."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/en-IN/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting product category."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/en-IN/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/en-IN/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/en-IN/deals'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The Dyson logo is visible
        await The 'Search products and parts' search box is present
        await The 'Shop now' button is visible
        await The 'Vacuum & wet cleaners' link is visible
        await The 'Air purifier' link is visible
        await The 'Headphones' link is visible
        await The 'Lighting' link is visible
        await The 'Support' link is visible
        await The 'Best sellers' link is visible