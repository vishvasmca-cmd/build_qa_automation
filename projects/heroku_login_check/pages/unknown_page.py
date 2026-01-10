from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the secure area page, displayed after successful login. It allows the user to logout.
    URL Pattern: https://the-internet.herokuapp.com/secure
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Logout Button(self):
        """Button to log out of the secure area."""
        return self.page.role=button[name="Logout"].or_(self.page.css=a.button)

    @property
    def Success Message(self):
        """Confirmation message displayed after successful login."""
        return self.page.css=#flash.or_(self.page.text=You logged into a secure area!)

    @property
    def Page Title(self):
        """The title of the secure area page."""
        return self.page.css=h2.or_(self.page.text=Secure Area)

    @property
    def Page Description(self):
        """Description of the secure area page."""
        return self.page.css=#content > h4.or_(self.page.text=Welcome to the Secure Area.)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Secure Area'
        await Success message is displayed: 'You logged into a secure area!'
        await Logout button is present
        await Page description is displayed: 'Welcome to the Secure Area. When you are done click logout below.'