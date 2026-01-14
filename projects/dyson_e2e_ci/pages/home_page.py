from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products, particularly the 'hushjet' purifier, and provide navigation to different product categories and information.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Link to return to the homepage."""
        return self.page.//a[@aria-label='Homepage'].or_(self.page.img[alt='Dyson'])

    @property
    def search_products_and_parts(self):
        """Search input field for products and parts."""
        return self.page.input[placeholder='Search products and parts'].or_(self.page.css=input[type='search'])

    @property
    def shop_now(self):
        """Button to navigate to the product page."""
        return self.page.//a[contains(text(),'Shop now')].or_(self.page.text=Shop now)

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.//a[contains(text(),'Deals')].or_(self.page.text=Deals)

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.//a[contains(text(),'Vacuum & wet cleaners')].or_(self.page.text=Vacuum & wet cleaners)

    @property
    def air_purifier(self):
        """Link to the air purifier page."""
        return self.page.//a[contains(text(),'Air purifier')].or_(self.page.text=Air purifier)

    @property
    def headphones(self):
        """Link to the headphones page."""
        return self.page.//a[contains(text(),'Headphones')].or_(self.page.text=Headphones)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson Official Website'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'