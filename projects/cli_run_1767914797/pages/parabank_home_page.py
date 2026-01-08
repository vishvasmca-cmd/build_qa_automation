from playwright.async_api import Page, expect

class ParabankHomePage:
    """
    Home page for ParaBank, featuring customer login and bank information.
    URL Pattern: /index.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for username."""
        return self.page.get_by_label('Username').or_(self.page.locator('input[name="username"]'))

    @property
    def password_input(self):
        """Input field for password."""
        return self.page.get_by_label('Password').or_(self.page.locator('input[name="password"]'))

    @property
    def login_button(self):
        """Button to submit login credentials."""
        return self.page.get_by_role('button', name='Log In').or_(self.page.locator('input[value="Log In"]'))

    @property
    def register_link(self):
        """Link to register a new account."""
        return self.page.get_by_role('link', name='Register').or_(self.page.locator('a[href="register.htm"]'))

    @property
    def forgot_login_info_link(self):
        """Link to recover login information."""
        return self.page.get_by_role('link', name='Forgot login info?').or_(self.page.locator('a[href="lookup.htm"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank | Welcome')
        await expect(page.get_by_text('Customer Login')).to_be_visible()
        await expect(page.get_by_text('Welcome to ParaBank')).to_be_visible()