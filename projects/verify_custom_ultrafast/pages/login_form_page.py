from playwright.async_api import Page, expect

class LoginFormPage:
    """
    This page is a standard login form, allowing users to enter their username and password to gain access to the application.
    URL Pattern: https://demo.applitools.com/app.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for the user to enter their username."""
        return self.page.username.or_(self.page.input[placeholder='Enter your username'])

    @property
    def Password Input(self):
        """Input field for the user to enter their password."""
        return self.page.password.or_(self.page.input[placeholder='Enter your password'])

    @property
    def Sign In Button(self):
        """Button to submit the login form."""
        return self.page.log-in.or_(self.page.button[id='log-in'])

    @property
    def Remember Me Checkbox(self):
        """Checkbox to remember the user's login details."""
        return self.page.remember-me.or_(self.page.label[for='remember-me'])

    @property
    def Login Form Title(self):
        """Title of the login form"""
        return self.page.Login Form.or_(self.page.h4)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ACME demo app'
        await Login Form title is displayed
        await Username input field is present
        await Password input field is present
        await Sign In button is present
        await Remember Me checkbox is present