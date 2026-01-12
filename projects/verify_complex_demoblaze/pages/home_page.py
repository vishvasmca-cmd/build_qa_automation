from playwright.async_api import Page, expect

class HomePage:
    """
    The home page of the Demoblaze online store, showcasing featured products and categories.
    URL Pattern: https://www.demoblaze.com/#
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_store_title(self):
        """The title of the store."""
        return self.page.xpath=//a[@class='navbar-brand'].or_(self.page.css=.navbar-brand)

    @property
    def home_link(self):
        """Link to the home page."""
        return self.page.link=Home.or_(self.page.css=a[href='index.html'])

    @property
    def contact_link(self):
        """Link to the contact page."""
        return self.page.link=Contact.or_(self.page.css=a[data-target='#exampleModal'])

    @property
    def about_us_link(self):
        """Link to the about us page."""
        return self.page.link=About us.or_(self.page.css=a[data-target='#videoModal'])

    @property
    def cart_link(self):
        """Link to the shopping cart."""
        return self.page.id=cartur.or_(self.page.link=Cart)

    @property
    def log_in_link(self):
        """Link to the login page."""
        return self.page.id=login2.or_(self.page.link=Log in)

    @property
    def sign_up_link(self):
        """Link to the sign up page."""
        return self.page.id=signin2.or_(self.page.link=Sign up)

    @property
    def phones_category(self):
        """Link to the phones category."""
        return self.page.link=Phones.or_(self.page.css=#itemc[href='prod.html?idp_=1'])

    @property
    def laptops_category(self):
        """Link to the laptops category."""
        return self.page.link=Laptops.or_(self.page.css=#itemc[href='prod.html?idp_=2'])

    @property
    def monitors_category(self):
        """Link to the monitors category."""
        return self.page.link=Monitors.or_(self.page.css=#itemc[href='prod.html?idp_=3'])

    @property
    def next_product(self):
        """Button to navigate to the next product in the carousel."""
        return self.page.xpath=//a[contains(@class, 'carousel-control-next')].or_(self.page.css=.carousel-control-next)

    @property
    def previous_product(self):
        """Button to navigate to the previous product in the carousel."""
        return self.page.xpath=//a[contains(@class, 'carousel-control-prev')].or_(self.page.css=.carousel-control-prev)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title contains 'STORE'
        await Verify the 'Product Store' title is visible
        await Verify the 'Home' link is visible
        await Verify at least one product is displayed