from playwright.async_api import Page, expect

class DysonIndiaOfficialWebsitePage:
    """
    This page displays Dyson's deals and product categories, showcasing their products and offers.
    URL Pattern: https://www.dyson.in/deals
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Products and Parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Shop Now Button(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=.button--primary)

    @property
    def Deals Link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def Vacuum & Wet Cleaners Link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def Hair Care Link(self):
        """Link to the hair care products page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care'])

    @property
    def Air Purifier Link(self):
        """Link to the air purifier products page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-treatment'])

    @property
    def Headphones Link(self):
        """Link to the headphones products page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def Lighting Link(self):
        """Link to the lighting products page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/lighting'])

    @property
    def Support Link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/support'])

    @property
    def Best Sellers Link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson India Official Website'
        await Header text 'Compact. Powerful. Yet quiet.' is visible
        await Element with text 'Shop now' is present
        await The text 'Dyson.in exclusive: 24 months no cost EMI' is visible