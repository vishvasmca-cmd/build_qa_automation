from playwright.async_api import Page, expect

class BrowserstackDemoLoginPage:
    """
    This is the login page for the BrowserStack demo application. It allows users to select a username and password from dropdown menus and log in.
    URL Pattern: https://bstackdemo.com/signin*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Dropdown(self):
        """Dropdown to select a username."""
        return self.page.id=username.or_(self.page.css=#username)

    @property
    def Password Dropdown(self):
        """Dropdown to select a password."""
        return self.page.id=password.or_(self.page.css=#password)

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.id=login-btn.or_(self.page.text=Log In)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'BrowserStack Demo'
        await Logo is visible
        await Username dropdown is present
        await Password dropdown is present
        await Login button is present