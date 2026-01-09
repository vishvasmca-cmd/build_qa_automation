from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the secure area page, accessible after successful login. It allows the user to logout.
    URL Pattern: https://the-internet.herokuapp.com/secure
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Success Message(self):
        """The success message displayed after successful login."""
        return self.page.text="You logged into a secure area!".or_(self.page.css=.flash.success)

    @property
    def Secure Area Header(self):
        """The main header of the secure area page."""
        return self.page.text="Secure Area".or_(self.page.css=h2)

    @property
    def Logout Button(self):
        """The logout button to return to the login page."""
        return self.page.text="Logout".or_(self.page.css=.button.secondary)

    @property
    def Powered by Elemental Selenium(self):
        """Link to Elemental Selenium website."""
        return self.page.text="Powered by Elemental Selenium".or_(self.page.css=div.example > p:nth-child(3) > a)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'The Internet'
        await Header text is 'Secure Area'
        await Logout button is present
        await Success message is displayed