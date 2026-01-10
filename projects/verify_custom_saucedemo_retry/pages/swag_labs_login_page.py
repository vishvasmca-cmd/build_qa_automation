from playwright.async_api import Page, expect

class SwagLabsLoginPage:
    """
    This is the login page for Swag Labs, where users can enter their credentials to access the inventory page.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for the username."""
        return self.page.[data-test='username'].or_(self.page.input#user-name)

    @property
    def Password Input(self):
        """Input field for the password."""
        return self.page.[data-test='password'].or_(self.page.input#password)

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.[data-test='login-button'].or_(self.page.input#login-button)

    @property
    def Accepted usernames(self):
        """Text displaying accepted usernames"""
        return self.page.//div[contains(text(),'Accepted usernames are:')].or_(self.page.div:nth-child(3))

    @property
    def Password for all users(self):
        """Text displaying password for all users"""
        return self.page.//div[contains(text(),'Password for all users:')].or_(self.page.div:nth-child(4))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Login button is present
        await Username input field is present
        await Password input field is present