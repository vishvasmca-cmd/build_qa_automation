from playwright.async_api import Page, expect

class DysonIndiaOfficialWebsitePage:
    """
    This page displays Dyson's deals and promotions, showcasing products like the 'hushjet' purifier.
    URL Pattern: https://www.dyson.in/deals
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Products and Parts(self):
        """Search input box to find products and parts."""
        return self.page.aria/Search products and parts.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Shop Now(self):
        """Button to navigate to the product page."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/purifiers/compact/hush-jet'])

    @property
    def Deals Link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def Vacuum & wet cleaners Link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def Hair care Link(self):
        """Link to the hair care products page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care'])

    @property
    def Air purifier Link(self):
        """Link to the air purifier products page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-purifiers'])

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
    def Best sellers Link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Deals and offers | Dyson India'
        await Header text 'Compact. Powerful. Yet quiet.' is visible
        await Element with text 'Dyson.in exclusive: 24 months no cost EMI' is visible