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
        return self.page.role=link[name='Dyson'].or_(self.page.css=a[aria-label='Homepage'])

    @property
    def search_products_and_parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox[name='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.role=link[name='Deals'].or_(self.page.text=Deals)

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum and wet cleaners page."""
        return self.page.role=link[name='Vacuum & wet cleaners'].or_(self.page.text='Vacuum & wet cleaners')

    @property
    def hair_care(self):
        """Link to the hair care products page."""
        return self.page.role=link[name='Hair care'].or_(self.page.text='Hair care')

    @property
    def air_purifier(self):
        """Link to the air purifier products page."""
        return self.page.role=link[name='Air purifier'].or_(self.page.text='Air purifier')

    @property
    def headphones(self):
        """Link to the headphones products page."""
        return self.page.role=link[name='Headphones'].or_(self.page.text='Headphones')

    @property
    def lighting(self):
        """Link to the lighting products page."""
        return self.page.role=link[name='Lighting'].or_(self.page.text='Lighting')

    @property
    def support(self):
        """Link to the support page."""
        return self.page.role=link[name='Support'].or_(self.page.text='Support')

    @property
    def best_sellers(self):
        """Link to the best sellers page."""
        return self.page.role=link[name='Best sellers'].or_(self.page.text='Best sellers')

    @property
    def shop_now(self):
        """Button to shop the featured product."""
        return self.page.text='Shop now'.or_(self.page.css=a[href='/en-IN/purifiers/compact'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Search products and parts'