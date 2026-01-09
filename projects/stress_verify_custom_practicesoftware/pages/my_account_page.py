from playwright.async_api import Page, expect

class MyAccountPage:
    """
    My Account page for login and registration
    URL Pattern: /my-account/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_email_address_input(self):
        """Input field for username or email address"""
        return self.page.get_by_label('Username or email address').or_(self.page.locator('#username'))

    @property
    def password_input(self):
        """Input field for password"""
        return self.page.get_by_label('Password').or_(self.page.locator('#password'))

    @property
    def login_button(self):
        """Button to submit the login form"""
        return self.page.get_by_role('button', name='Login').or_(self.page.locator('input[name="login"]'))

    @property
    def remember_me_checkbox(self):
        """Checkbox to remember the user"""
        return self.page.get_by_label('Remember me').or_(self.page.locator('#rememberme'))

    @property
    def lost_password_link(self):
        """Link to reset the password"""
        return self.page.get_by_text('Lost your password?').or_(self.page.locator('a[href*="lost-password"]'))

    @property
    def register_email_address_input(self):
        """Input field for registration email address"""
        return self.page.get_by_label('Email address').or_(self.page.locator('#reg_email'))

    @property
    def register_password_input(self):
        """Input field for registration password"""
        return self.page.get_by_label('Password', exact=True).nth(1).or_(self.page.locator('#reg_password'))

    @property
    def register_button(self):
        """Button to submit the registration form"""
        return self.page.get_by_role('button', name='Register').or_(self.page.locator('input[name="register"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('My Account – Automation Practice')
        await expect(page.get_by_role('heading', name='Login').first()).to_be_visible()
        await expect(page.get_by_role('heading', name='Register').first()).to_be_visible()