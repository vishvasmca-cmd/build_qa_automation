from playwright.async_api import Page, expect

class ParabankHomePage:
    """
    ParaBank Home Page - Customer Login
    URL Pattern: /parabank/index.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for username"""
        return self.page.get_by_label('Username').or_(self.page.locator('[name="username"]'))

    @property
    def password_input(self):
        """Input field for password"""
        return self.page.get_by_label('Password').or_(self.page.locator('[name="password"]'))

    @property
    def login_button(self):
        """Button to submit login credentials"""
        return self.page.get_by_role('button', name='Log In').or_(self.page.locator('[value="Log In"]'))

    @property
    def register_link(self):
        """Link to register a new user account"""
        return self.page.get_by_role('link', name='Register').or_(self.page.locator('a:has-text("Register")'))

    @property
    def forgot_login_info_link(self):
        """Link to recover login credentials"""
        return self.page.get_by_role('link', name='Forgot login info?').or_(self.page.locator('a:has-text("Forgot login info?")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank | Welcome | Online Banking')
        await expect(page.locator('//h2[text()="Customer Login"]')).to_be_visible()
        await expect(page.locator('//img[@title="ParaBank"]')).to_be_visible()