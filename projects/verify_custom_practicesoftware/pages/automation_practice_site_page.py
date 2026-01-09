from playwright.async_api import Page, expect

class AutomationPracticeSitePage:
    """
    This is the home page of the Automation Practice Site, showcasing available books and navigation links.
    URL Pattern: https://practice.automationtesting.in/my-account/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Shop Link(self):
        """Link to the shop page."""
        return self.page.link=Shop.or_(self.page.css=li#menu-item-50 > a)

    @property
    def My Account Link(self):
        """Link to the My Account page."""
        return self.page.link=My Account.or_(self.page.css=li#menu-item-50 > a)

    @property
    def Test Cases Link(self):
        """Link to the Test Cases page."""
        return self.page.link=Test Cases.or_(self.page.css=li#menu-item-50 > a)

    @property
    def AT Site Link(self):
        """Link to the AT Site page."""
        return self.page.link=AT Site.or_(self.page.css=li#menu-item-50 > a)

    @property
    def Demo Site Link(self):
        """Link to the Demo Site page."""
        return self.page.link=Demo Site.or_(self.page.css=li#menu-item-50 > a)

    @property
    def Cart Items(self):
        """Link to the shopping cart."""
        return self.page.css=.cart-contents.or_(self.page.text=0 Items - P0.00)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'My Account – Automation Practice Site'
        await Presence of 'Shop' link
        await Presence of 'My Account' link
        await Presence of 'Test Cases' link
        await Presence of 'AT Site' link
        await Presence of 'Demo Site' link
        await Presence of '0 Items - P0.00' text