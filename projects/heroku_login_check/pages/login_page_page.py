from playwright.async_api import Page, expect

class LoginPagePage:
    """
    This is the login page for the-internet.herokuapp.com/secure. It allows users to enter their username and password to access the secure area.
    URL Pattern: https://the-internet.herokuapp.com/secure
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for the username."""
        return self.page.id=username.or_(self.page.css=input[name='username'])

    @property
    def Password Input(self):
        """Input field for the password."""
        return self.page.id=password.or_(self.page.css=input[name='password'])

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.css=button[type='submit'].or_(self.page.id=login)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page contains the 'Login Page' header.
        await Username input field is present.
        await Password input field is present.
        await Login button is present.