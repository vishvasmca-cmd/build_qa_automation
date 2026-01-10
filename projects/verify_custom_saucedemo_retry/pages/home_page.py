from playwright.async_api import Page, expect

class HomePage:
    """
    This is the login page for the Swag Labs demo application.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for the username."""
        return self.page.[data-test='username'].or_(self.page.input[id='user-name'])

    @property
    def Password Input(self):
        """Input field for the password."""
        return self.page.[data-test='password'].or_(self.page.input[id='password'])

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.[data-test='login-button'].or_(self.page.input[id='login-button'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Login button is present
        await Username input field is present
        await Password input field is present