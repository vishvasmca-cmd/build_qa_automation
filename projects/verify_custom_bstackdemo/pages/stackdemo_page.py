from playwright.async_api import Page, expect

class StackdemoPage:
    """
    This page is the sign-in page for the BrowserStack demo application. It allows users to select a username and password from dropdown menus and log in.
    URL Pattern: https://bstackdemo.com/signin?checkout=true
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Dropdown(self):
        """Dropdown menu to select a username."""
        return self.page.id=username.or_(self.page.css=select[name='username'])

    @property
    def Password Dropdown(self):
        """Dropdown menu to select a password."""
        return self.page.id=password.or_(self.page.css=select[name='password'])

    @property
    def Log In Button(self):
        """Button to submit the login form."""
        return self.page.id=login-btn.or_(self.page.css=#login-btn)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'BrowserStack Demo'
        await The 'Select Username' dropdown is present
        await The 'Select Password' dropdown is present
        await The 'Log In' button is present