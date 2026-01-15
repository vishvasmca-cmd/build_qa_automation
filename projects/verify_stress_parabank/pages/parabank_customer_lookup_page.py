from playwright.async_api import Page, expect

class ParabankCustomerLookupPage:
    """
    The ParaBank Home Page allows users to log in, view services, and access information about the bank.
    URL Pattern: https://parabank.parasoft.com/parabank/index.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for entering the username."""
        return self.page.username.or_(self.page.css=input[name='username'])

    @property
    def password_input(self):
        """Input field for entering the password."""
        return self.page.password.or_(self.page.css=input[name='password'])

    @property
    def log_in_button(self):
        """Button to submit the login form."""
        return self.page.login.or_(self.page.css=input[value='Log In'])

    @property
    def forgot_login_info_link(self):
        """Link to navigate to the forgot login info page."""
        return self.page.Forgot login info?.or_(self.page.css=#loginPanel > p:nth-child(3) > a)

    @property
    def register_link(self):
        """Link to navigate to the registration page."""
        return self.page.Register.or_(self.page.css=#loginPanel > p:nth-child(4) > a)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'ParaBank'
        await Presence of 'Customer Login' heading
        await Presence of 'Username' input field
        await Presence of 'Password' input field
        await Presence of 'Log In' button