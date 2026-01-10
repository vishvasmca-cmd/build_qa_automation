from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the login page for Swag Labs, where users can enter their username and password to access the application.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for the username."""
        return self.page.//input[@id='user-name'].or_(self.page.css=input#user-name)

    @property
    def Password Input(self):
        """Input field for the password."""
        return self.page.//input[@id='password'].or_(self.page.css=input#password)

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.//input[@id='login-button'].or_(self.page.css=input#login-button)

    @property
    def Accepted usernames(self):
        """Text displaying accepted usernames."""
        return self.page.//div[@id='login_credentials'].or_(self.page.text=Accepted usernames are:)

    @property
    def Password for all users(self):
        """Text displaying the password for all users."""
        return self.page.//div[@class='login_password'].or_(self.page.text=Password for all users:)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Login button is present
        await Username input field is present
        await Password input field is present
        await The text 'Accepted usernames are:' is present
        await The text 'Password for all users:' is present