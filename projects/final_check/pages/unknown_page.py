from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the login page for the Swag Labs application, where users can enter their credentials to access the application's features.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for the username."""
        return self.page.id=user-name.or_(self.page.css=input[placeholder='Username'])

    @property
    def Password Input(self):
        """Input field for the password."""
        return self.page.id=password.or_(self.page.css=input[placeholder='Password'])

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.id=login-button.or_(self.page.css=input[value='Login'])

    @property
    def Accepted usernames(self):
        """Text displaying accepted usernames"""
        return self.page.text=Accepted usernames are:.or_(self.page.css=.login_credentials)

    @property
    def Password for all users(self):
        """Text displaying password for all users"""
        return self.page.text=Password for all users:.or_(self.page.css=.password)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Login button is present and enabled
        await Username and password input fields are present
        await The text 'Accepted usernames are:' is displayed
        await The text 'Password for all users:' is displayed