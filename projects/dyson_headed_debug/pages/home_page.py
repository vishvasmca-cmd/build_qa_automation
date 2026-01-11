from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. It showcases products and provides navigation to different sections of the website.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Products(self):
        """Search input field for products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Shop Now(self):
        """Button to navigate to the Hushjet purifier product page."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/en-IN/air-treatment/air-purifiers/hush-jet'])

    @property
    def Deals(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/en-IN/deals'])

    @property
    def Vacuum & wet cleaners(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/en-IN/vacuum-cleaners'])

    @property
    def Hair care(self):
        """Link to the hair care products page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/en-IN/hair-care'])

    @property
    def Air purifier(self):
        """Link to the air purifier products page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/en-IN/air-treatment'])

    @property
    def Headphones(self):
        """Link to the headphones products page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/en-IN/headphones'])

    @property
    def Lighting(self):
        """Link to the lighting products page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/en-IN/lighting'])

    @property
    def Support(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/en-IN/support'])

    @property
    def Best sellers(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/en-IN/best-sellers'])

    @property
    def Discover Dyson(self):
        """Link to the Discover Dyson page."""
        return self.page.text=Discover Dyson.or_(self.page.css=a[href='/en-IN/dyson-technology'])

    @property
    def For business(self):
        """Link to the For business page."""
        return self.page.text=For business.or_(self.page.css=a[href='/en-IN/for-business'])

    @property
    def Store finder(self):
        """Link to the Store finder page."""
        return self.page.text=Store finder.or_(self.page.css=a[href='/en-IN/store-finder'])

    @property
    def Register machine(self):
        """Link to the Register machine page."""
        return self.page.text=Register machine.or_(self.page.css=a[href='/en-IN/support/your-dyson/registration'])

    @property
    def Contact us(self):
        """Link to the Contact us page."""
        return self.page.text=Contact us.or_(self.page.css=a[href='/en-IN/support/contact-us'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson'
        await Page contains the text 'Compact. Powerful. Yet quiet.'
        await Page contains the text 'Dyson.in exclusive: 24 months no cost EMI'