from playwright.async_api import Page, expect

class HomePage:
    """
    Login page for Swag Labs application
    URL Pattern: /login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self):
        """Input field for username"""
        return self.page.get_by_text('Username').or_(self.page.locator('#user-name'))

    @property
    def password_field(self):
        """Input field for password"""
        return self.page.get_by_text('Password').or_(self.page.locator('#password'))

    @property
    def login_button(self):
        """Button to submit login credentials"""
        return self.page.get_by_role('button', name='Login').or_(self.page.locator('#login-button'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Swag Labs')
        await expect(page.locator('#login-button')).to_be_visible()
        await expect(page.locator('#user-name')).to_be_visible()
        await expect(page.locator('#password')).to_be_visible()