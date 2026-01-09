from playwright.async_api import Page, expect

class LoginPage:
    """
    Login page for OrangeHRM application
    URL Pattern: /auth/login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self):
        """Input field for username"""
        return self.page.get_by_placeholder('Username').or_(self.page.locator('input[name="username"]'))

    @property
    def password_field(self):
        """Input field for password"""
        return self.page.get_by_placeholder('Password').or_(self.page.locator('input[name="password"]'))

    @property
    def login_button(self):
        """Button to submit login credentials"""
        return self.page.get_by_role('button', name='Login').or_(self.page.locator('button[type="submit"]'))

    @property
    def forgot_password_link(self):
        """Link to navigate to the forgot password page"""
        return self.page.get_by_text('Forgot your password?').or_(self.page.locator('p.oxd-text.oxd-text--p.orangehrm-login-forgot-header'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Login')).to_be_visible()