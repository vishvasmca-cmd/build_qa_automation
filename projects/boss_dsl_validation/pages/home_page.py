from playwright.async_api import Page, expect

class HomePage:
    """
    This is the login page for the Swag Labs e-commerce website. Users can enter their username and password to access the product catalog.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for username."""
        return self.page.[data-test="username"].or_(self.page.input#user-name)

    @property
    def password_input(self):
        """Input field for password."""
        return self.page.[data-test="password"].or_(self.page.input#password)

    @property
    def login_button(self):
        """Button to submit login credentials."""
        return self.page.[data-test="login-button"].or_(self.page.input#login-button)

    @property
    def accepted_usernames_are_(self):
        """Text displaying accepted usernames."""
        return self.page.text=Accepted usernames are:.or_(self.page.div.login_credentials)

    @property
    def password_for_all_users_(self):
        """Text displaying password for all users."""
        return self.page.text=Password for all users:.or_(self.page.div.password)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Username input field is present
        await Password input field is present
        await Login button is present
        await Accepted usernames text is present
        await Password for all users text is present