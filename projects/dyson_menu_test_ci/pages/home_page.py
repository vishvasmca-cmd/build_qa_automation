from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. It showcases Dyson products and provides navigation to different product categories and support resources.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Products(self):
        """Search input field for products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Deals Link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals.html'])

    @property
    def Vacuum & wet cleaners Link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners.html'])

    @property
    def Hair care Link(self):
        """Link to the hair care products page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care.html'])

    @property
    def Air purifier Link(self):
        """Link to the air purifiers page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-purifiers.html'])

    @property
    def Headphones Link(self):
        """Link to the headphones page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones.html'])

    @property
    def Lighting Link(self):
        """Link to the lighting products page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/lighting.html'])

    @property
    def Support Link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/support.html'])

    @property
    def Best sellers Link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers.html'])

    @property
    def Shop now button(self):
        """Button to navigate to the hushjet air purifier page."""
        return self.page.text=Shop now.or_(self.page.css=a[class='button'][href='/air-purifiers/hushjet.html'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson India'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'