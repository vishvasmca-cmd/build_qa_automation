from playwright.async_api import Page, expect

class DysonIndiaOfficialWebsitePage:
    """
    This is the homepage of Dyson India's official website. The primary purpose is to showcase Dyson products and provide navigation to different product categories and information.
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
        """Button to navigate to the product details page."""
        return self.page.text=Shop now.or_(self.page.css=.button.button--green)

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners product category page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href*='/vacuum-cleaners'])

    @property
    def headphones_link(self):
        """Link to the headphones product category page."""
        return self.page.text=Headphones.or_(self.page.css=a[href*='/headphones'])

    @property
    def dyson_logo(self):
        """Dyson logo that usually navigates to the homepage."""
        return self.page.css=svg[aria-label='Dyson'].or_(self.page.alt=Dyson)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson India Official Website'
        await Header text 'Compact. Powerful. Yet quiet.' is visible
        await The 'Shop now' button is visible
        await The Dyson logo is visible