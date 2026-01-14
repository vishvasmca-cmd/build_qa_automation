from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to showcase Dyson products and promotions, particularly focusing on hair care products in this instance. It also provides navigation to different product categories and support resources.
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
        """Button to navigate to the hair care product section."""
        return self.page.text=Shop now.or_(self.page.css=a[href*='/hair-care'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners product category."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href*='/vacuum-cleaners'])

    @property
    def hair_care_link(self):
        """Link to the hair care product category."""
        return self.page.text=Hair care.or_(self.page.css=a[href*='/hair-care'])

    @property
    def headphones_link(self):
        """Link to the headphones product category."""
        return self.page.text=Headphones.or_(self.page.css=a[href*='/headphones'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href*='/support'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href*='/deals'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson India'
        await The main header text 'This wedding season, the difference is Dyson' is present
        await The 'Shop now' button is visible
        await The Dyson logo is visible