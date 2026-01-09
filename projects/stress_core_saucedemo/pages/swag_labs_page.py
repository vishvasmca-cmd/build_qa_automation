from playwright.async_api import Page, expect

class SwagLabsPage:
    """
    Login page for customer access
    URL Pattern: /login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self):
        """Username input field"""
        return self.page.get_by_text('standard_user').or_(self.page.locator('input[placeholder="Username"]'))

    @property
    def password_field(self):
        """Password input field"""
        return self.page.get_by_text('secret_sauce').or_(self.page.locator('input[placeholder="Password"]'))

    @property
    def login_button(self):
        """Main submission button"""
        return self.page.get_by_role('button', name='Login').or_(self.page.locator('#login-button'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Swag Labs')
        await expect(page.get_by_role('button', name='Login')).to_be_visible()