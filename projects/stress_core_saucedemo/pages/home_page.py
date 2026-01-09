from playwright.async_api import Page, expect

class HomePage:
    """
    This is the login page for the Swag Labs e-commerce website. Users can enter their username and password to access the product catalog.
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
    def Accepted usernames are:(self):
        """Text displaying accepted usernames"""
        return self.page.text=Accepted usernames are:.or_(self.page.div.login_credentials_wrap > div > div.login_credentials)

    @property
    def Password for all users:(self):
        """Text displaying password for all users"""
        return self.page.text=Password for all users:.or_(self.page.div.login_password)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Login button is present
        await Username input field is present
        await Password input field is present