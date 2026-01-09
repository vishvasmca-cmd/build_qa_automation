from playwright.async_api import Page, expect

class LoginFormPage:
    """
    This is the login form page for the demo app.
    URL Pattern: https://demo.applitools.com/app.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for username"""
        return self.page.id=username.or_(self.page.css=input[placeholder='Enter your username'])

    @property
    def Password Input(self):
        """Input field for password"""
        return self.page.id=password.or_(self.page.css=input[placeholder='Enter your password'])

    @property
    def Sign In Button(self):
        """Button to submit the login form"""
        return self.page.id=log-in.or_(self.page.css=#log-in)

    @property
    def Remember Me Checkbox(self):
        """Checkbox to remember the user"""
        return self.page.class=form-check-input.or_(self.page.text=Remember Me)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ACME demo app'
        await Login Form header is present
        await Username input field is present
        await Password input field is present
        await Sign In button is present