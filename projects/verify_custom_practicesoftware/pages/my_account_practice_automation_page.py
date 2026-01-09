from playwright.async_api import Page, expect

class MyAccountPracticeAutomationPage:
    """
    This page allows users to log in to their existing account or register for a new account.
    URL Pattern: https://practice.automationtesting.in/my-account/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username or email address input(self):
        """Input field for username or email address for login."""
        return self.page.//input[@id='username'].or_(self.page.css=#username)

    @property
    def Password input (Login)(self):
        """Input field for password for login."""
        return self.page.//input[@id='password'].or_(self.page.css=#password)

    @property
    def Login button(self):
        """Button to submit the login form."""
        return self.page.//input[@name='login'].or_(self.page.css=[name='login'])

    @property
    def Remember me checkbox(self):
        """Checkbox to remember the user's login details."""
        return self.page.//input[@id='rememberme'].or_(self.page.css=#rememberme)

    @property
    def Lost your password link(self):
        """Link to navigate to the password reset page."""
        return self.page.//a[contains(text(),'Lost your password?')].or_(self.page.text=Lost your password?)

    @property
    def Email address input (Register)(self):
        """Input field for email address for registration."""
        return self.page.//input[@id='reg_email'].or_(self.page.css=#reg_email)

    @property
    def Password input (Register)(self):
        """Input field for password for registration."""
        return self.page.//input[@id='reg_password'].or_(self.page.css=#reg_password)

    @property
    def Register button(self):
        """Button to submit the registration form."""
        return self.page.//input[@name='register'].or_(self.page.css=[name='register'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'My Account - Practice Automation'
        await Login heading is displayed
        await Register heading is displayed