from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage of Dyson India. The primary purpose is to showcase products, particularly the 'hushjet Purifier Compact', and provide navigation to different product categories and support resources.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Link to the Dyson homepage."""
        return self.page.//a[@aria-label='Dyson'].or_(self.page.css=a.header__logo-link)

    @property
    def search_products_and_parts(self):
        """Search input field for products and parts."""
        return self.page.css=input[placeholder='Search products and parts'].or_(self.page.//input[@placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the product page of 'hushjet Purifier Compact'."""
        return self.page.//a[contains(text(),'Shop now')].or_(self.page.css=a.button.button--green)

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.//a[contains(text(),'Deals')].or_(self.page.text=Deals)

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum and wet cleaners page."""
        return self.page.//a[contains(text(),'Vacuum & wet cleaners')].or_(self.page.text='Vacuum & wet cleaners')

    @property
    def hair_care_link(self):
        """Link to the hair care products page."""
        return self.page.//a[contains(text(),'Hair care')].or_(self.page.text='Hair care')

    @property
    def air_purifier_link(self):
        """Link to the air purifier products page."""
        return self.page.//a[contains(text(),'Air purifier')].or_(self.page.text='Air purifier')

    @property
    def headphones_link(self):
        """Link to the headphones products page."""
        return self.page.//a[contains(text(),'Headphones')].or_(self.page.text='Headphones')

    @property
    def lighting_link(self):
        """Link to the lighting products page."""
        return self.page.//a[contains(text(),'Lighting')].or_(self.page.text='Lighting')

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.//a[contains(text(),'Support')].or_(self.page.text='Support')

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.//a[contains(text(),'Best sellers')].or_(self.page.text='Best sellers')

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await The 'hushjet Purifier Compact' section is displayed
        await The 'Search products and parts' search box is present
        await The Dyson logo is visible