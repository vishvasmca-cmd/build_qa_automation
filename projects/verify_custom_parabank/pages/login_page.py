from playwright.async_api import Page, expect

class LoginPage:
    """
    This is the Login page for ParaBank, where users can enter their credentials to access their accounts.
    URL Pattern: https://parabank.parasoft.com/parabank/login.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for entering the username."""
        return self.page.id=username.or_(self.page.name=username)

    @property
    def password_input(self):
        """Input field for entering the password."""
        return self.page.id=password.or_(self.page.name=password)

    @property
    def log_in_button(self):
        """Button to submit the login form."""
        return self.page.css=input[value='Log In'].or_(self.page.xpath=//input[@value='Log In'])

    @property
    def forgot_login_info_link(self):
        """Link to navigate to the 'Forgot Login Info' page."""
        return self.page.link=Forgot login info?.or_(self.page.css=a[href*='lookup'])

    @property
    def register_link(self):
        """Link to navigate to the registration page."""
        return self.page.link=Register.or_(self.page.css=a[href*='register'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ParaBank Login'
        await Page contains the header 'Customer Login'
        await Username input field is present
        await Password input field is present
        await Log In button is present