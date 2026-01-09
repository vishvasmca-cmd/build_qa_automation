from playwright.async_api import Page, expect

class HomePage:
    """
    Login page for Swag Labs customer access
    URL Pattern: /
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self):
        """Field to enter username"""
        return self.page.get_by_test_id('username').or_(self.page.locator('#user-name'))

    @property
    def password_field(self):
        """Field to enter password"""
        return self.page.get_by_test_id('password').or_(self.page.locator('#password'))

    @property
    def login_button(self):
        """Button to submit login credentials"""
        return self.page.get_by_test_id('login-button').or_(self.page.locator('#login-button'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Swag Labs')
        await expect(page.locator('.login_logo')).to_be_visible()
        await expect(page.locator('.login_wrapper')).to_be_visible()