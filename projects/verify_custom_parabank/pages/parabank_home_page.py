from playwright.async_api import Page, expect

class ParabankHomePage:
    """
    The ParaBank Home Page is the entry point for users to access various banking services, including account login, registration, and information about available services.
    URL Pattern: https://parabank.parasoft.com/parabank/index.htm*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for entering the username."""
        return self.page.id=username.or_(self.page.css=input[name='username'])

    @property
    def password_input(self):
        """Input field for entering the password."""
        return self.page.id=password.or_(self.page.css=input[name='password'])

    @property
    def log_in_button(self):
        """Button to submit the login form."""
        return self.page.css=input[value='Log In'].or_(self.page.xpath=//input[@value='Log In'])

    @property
    def register_link(self):
        """Link to navigate to the registration page."""
        return self.page.link=Register.or_(self.page.css=a[href='register.htm'])

    @property
    def forgot_login_info_link(self):
        """Link to navigate to the forgot login info page."""
        return self.page.link=Forgot login info?.or_(self.page.css=a[href*='lookupcustomer'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'ParaBank'
        await Presence of 'Welcome to ParaBank' text
        await Presence of 'Customer Login' section