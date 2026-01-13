from playwright.async_api import Page, expect

class LoginPage:
    """
    This is the login page for OrangeHRM. Users can enter their username and password to access the system.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for the username."""
        return self.page.[name='username'].or_(self.page.input[placeholder='Username'])

    @property
    def password_input(self):
        """Input field for the password."""
        return self.page.[name='password'].or_(self.page.input[placeholder='Password'])

    @property
    def login_button(self):
        """Button to submit the login form."""
        return self.page.button[type='submit'].or_(self.page.button:has-text('Login'))

    @property
    def forgot_your_password_(self):
        """Link to navigate to the 'Forgot Password' page."""
        return self.page.a:has-text('Forgot your password?').or_(self.page.p.oxd-text.oxd-text--p.orangehrm-login-forgot-header)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'OrangeHRM'
        await Login header is visible
        await Username input field is present
        await Password input field is present
        await Login button is present