from playwright.async_api import Page, expect

class SwagLabsPage:
    """
    This is the login page for Swag Labs, where users can enter their credentials to access the inventory.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for the username."""
        return self.page.id=user-name.or_(self.page.css=input[placeholder='Username'])

    @property
    def password_input(self):
        """Input field for the password."""
        return self.page.id=password.or_(self.page.css=input[placeholder='Password'])

    @property
    def login_button(self):
        """Button to submit the login form."""
        return self.page.id=login-button.or_(self.page.css=input[value='Login'])

    @property
    def accepted_usernames(self):
        """Text indicating the accepted usernames."""
        return self.page.xpath=//div[text()='Accepted usernames are:'].or_(self.page.text=Accepted usernames are:)

    @property
    def password_for_all_users(self):
        """Text indicating the password for all users."""
        return self.page.xpath=//div[text()='Password for all users:'].or_(self.page.text=Password for all users:)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Login button is present
        await Username input field is present
        await Password input field is present
        await Accepted usernames text is present
        await Password for all users text is present