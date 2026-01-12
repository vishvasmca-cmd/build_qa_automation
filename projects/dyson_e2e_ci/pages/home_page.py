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
        """Dyson logo in the top left corner, navigates to the homepage."""
        return self.page.role=link[name='Homepage'].or_(self.page.css=svg[aria-label='Dyson'])

    @property
    def search_products_and_parts(self):
        """Search input field to search for products and parts."""
        return self.page.role=searchbox[name='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the product page of the featured product."""
        return self.page.role=link[name='Shop now'].or_(self.page.text=Shop now)

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum and wet cleaners product category."""
        return self.page.role=link[name='Vacuum & wet cleaners'].or_(self.page.text='Vacuum & wet cleaners')

    @property
    def air_purifier(self):
        """Link to the air purifier product category."""
        return self.page.role=link[name='Air purifier'].or_(self.page.text='Air purifier')

    @property
    def headphones(self):
        """Link to the headphones product category."""
        return self.page.role=link[name='Headphones'].or_(self.page.text='Headphones')

    @property
    def lighting(self):
        """Link to the lighting product category."""
        return self.page.role=link[name='Lighting'].or_(self.page.text='Lighting')

    @property
    def support(self):
        """Link to the support page."""
        return self.page.role=link[name='Support'].or_(self.page.text='Support')

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.role=link[name='Best sellers'].or_(self.page.text='Best sellers')

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title contains 'Dyson India'
        await Verify the Dyson logo is visible
        await Verify the 'Search products and parts' search box is present
        await Verify the 'Shop now' button is visible
        await Verify the 'Dyson.in exclusive: 24 months no cost EMI' text is visible