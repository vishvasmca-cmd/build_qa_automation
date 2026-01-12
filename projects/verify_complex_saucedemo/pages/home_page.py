from playwright.async_api import Page, expect

class HomePage:
    """
    This is the login page for Swag Labs, where users can enter their credentials to access the inventory.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for the username."""
        return self.page.[data-test="username"].or_(self.page.input#user-name)

    @property
    def password_input(self):
        """Input field for the password."""
        return self.page.[data-test="password"].or_(self.page.input#password)

    @property
    def login_button(self):
        """Button to submit the login form."""
        return self.page.[data-test="login-button"].or_(self.page.input#login-button)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Username input field is present
        await Password input field is present
        await Login button is present