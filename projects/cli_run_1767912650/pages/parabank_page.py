from playwright.async_api import Page, expect

class ParabankPage:
    """
    Login page for customer access to ParaBank
    URL Pattern: /login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for username"""
        return self.page.get_by_label('Username').or_(self.page.locator('input[name="username"]'))

    @property
    def password_input(self):
        """Input field for password"""
        return self.page.get_by_label('Password').or_(self.page.locator('input[name="password"]'))

    @property
    def login_button(self):
        """Main submission button for login"""
        return self.page.get_by_role('button', name='Log In').or_(self.page.locator('input[value="Log In"]'))

    @property
    def forgot_login_info_link(self):
        """Link to recover login information"""
        return self.page.get_by_text('Forgot login info?').or_(self.page.locator('a[href="lookup.htm"]'))

    @property
    def register_link(self):
        """Link to register a new account"""
        return self.page.get_by_text('Register').or_(self.page.locator('a[href="register.htm"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank')
        await expect(page.get_by_text('Customer Login')).to_be_visible()
        await expect(page.locator('input[name="username"]')).to_be_visible()
        await expect(page.locator('input[name="password"]')).to_be_visible()
        await expect(page.locator('input[value="Log In"]')).to_be_visible()