from playwright.async_api import Page, expect

class DysonIndiaPage:
    """
    This is the Dyson India homepage, primarily used for showcasing and selling Dyson products, particularly vacuum cleaners and air purifiers. It also provides access to other product categories and support resources.
    URL Pattern: https://www.dyson.in/vacuum-cleaners
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now(self):
        """Button to navigate to the purifier product page."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/purifiers/compact'])

    @property
    def vacuum_wet_cleaners(self):
        """Link to the vacuum cleaners product category page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/offers'])

    @property
    def air_purifier(self):
        """Link to the air purifier product category page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-purifiers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Header text 'Compact. Powerful. Yet quiet.' is visible
        await The 'Search products and parts' search box is present
        await The 'Shop now' button is present