from playwright.async_api import Page, expect

class ParabankPage:
    """
    This is the ParaBank Home page, which allows users to log in, register, and access information about the bank's services.
    URL Pattern: https://parabank.parasoft.com/parabank/index.htm*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username(self):
        """Input field for the user's username."""
        return self.page.id=username.or_(self.page.css=[name='username'])

    @property
    def Password(self):
        """Input field for the user's password."""
        return self.page.id=password.or_(self.page.css=[name='password'])

    @property
    def Log In(self):
        """Button to submit the login form."""
        return self.page.css=[value='Log In'].or_(self.page.xpath=//input[@value='Log In'])

    @property
    def Register(self):
        """Link to navigate to the registration page."""
        return self.page.linkText=Register.or_(self.page.css=[href='register.htm'])

    @property
    def Forgot login info?(self):
        """Link to navigate to the password recovery page."""
        return self.page.linkText=Forgot login info?.or_(self.page.css=[href*='lookupcustomer'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'ParaBank'
        await Presence of 'Customer Login' heading
        await Presence of 'Welcome to ParaBank' banner