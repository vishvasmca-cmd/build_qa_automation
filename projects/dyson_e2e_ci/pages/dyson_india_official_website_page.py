from playwright.async_api import Page, expect

class DysonIndiaOfficialWebsitePage:
    """
    This page is the homepage of Dyson India, showcasing their products and promotions.
    URL Pattern: https://www.dyson.in/*
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
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/en-IN/purifiers/compact/hush-jet'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners category page."""
        return self.page.text='Vacuum & wet cleaners'.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier category page."""
        return self.page.text='Air purifier'.or_(self.page.css=a[href='/air-purifiers'])

    @property
    def headphones_link(self):
        """Link to the headphones category page."""
        return self.page.text='Headphones'.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting category page."""
        return self.page.text='Lighting'.or_(self.page.css=a[href='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text='Support'.or_(self.page.css=a[href='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text='Best sellers'.or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'