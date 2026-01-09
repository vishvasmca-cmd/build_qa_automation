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
        return self.page.role=textbox[name="Username"].or_(self.page.css=input[id="user-name"])

    @property
    def Password Input(self):
        """Input field for the password."""
        return self.page.role=textbox[name="Password"].or_(self.page.css=input[id="password"])

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.role=button[name="Login"].or_(self.page.css=input[id="login-button"])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Login button is present
        await Username input field is present
        await Password input field is present