from playwright.async_api import Page, expect

class ParabankPage:
    """
    This page is the ParaBank homepage, providing access to customer login, services, and information.
    URL Pattern: https://parabank.parasoft.com/parabank/index.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for entering the username."""
        return self.page.//input[@name='username'].or_(self.page.css=input[name='username'])

    @property
    def Password Input(self):
        """Input field for entering the password."""
        return self.page.//input[@name='password'].or_(self.page.css=input[name='password'])

    @property
    def Log In Button(self):
        """Button to submit the login form."""
        return self.page.//input[@value='Log In'].or_(self.page.css=input[value='Log In'])

    @property
    def Register Link(self):
        """Link to navigate to the registration page."""
        return self.page.//a[contains(text(),'Register')].or_(self.page.text=Register)

    @property
    def Forgot login info? Link(self):
        """Link to navigate to the forgot login info page."""
        return self.page.//a[contains(text(),'Forgot login info?')].or_(self.page.text=Forgot login info?)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'ParaBank'
        await Page contains the text 'Customer Login'
        await Page contains the text 'Welcome to ParaBank'