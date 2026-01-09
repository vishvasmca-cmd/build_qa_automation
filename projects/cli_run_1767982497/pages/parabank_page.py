from playwright.async_api import Page, expect

class ParabankPage:
    """
    Login page for customer access
    URL Pattern: /login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self):
        """Input field for username"""
        return self.page.get_by_label('Username').or_(self.page.locator('input[name="username"]'))

    @property
    def password_field(self):
        """Input field for password"""
        return self.page.get_by_label('Password').or_(self.page.locator('input[name="password"]'))

    @property
    def login_button(self):
        """Main submission button"""
        return self.page.get_by_role('button', name='LOG IN').or_(self.page.locator('input[value="Log In"]'))

    @property
    def register_link(self):
        """Link to registration page"""
        return self.page.get_by_role('link', name='Register').or_(self.page.locator('a[href="register.htm"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank')
        await expect(page.locator('//h2[text()="Customer Login"]')).to_be_visible()