from playwright.async_api import Page, expect

class ParabankHomePage:
    """
    Home page for ParaBank with customer login and links to services
    URL Pattern: /parabank/index.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_field(self):
        """Input field for the user's username"""
        return self.page.get_by_label('Username').or_(self.page.locator('input[name="username"]'))

    @property
    def password_field(self):
        """Input field for the user's password"""
        return self.page.get_by_label('Password').or_(self.page.locator('input[name="password"]'))

    @property
    def login_button(self):
        """Button to submit the login form"""
        return self.page.get_by_role('button', name='Log In').or_(self.page.locator('input[value="Log In"]'))

    @property
    def register_link(self):
        """Link to the registration page"""
        return self.page.get_by_role('link', name='Register').or_(self.page.locator('a[href="register.htm"]'))

    @property
    def forgot_login_info_link(self):
        """Link to the forgot login info page"""
        return self.page.get_by_role('link', name='Forgot login info?').or_(self.page.locator('a[href="lookupcustomer.htm"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank | Welcome')
        await expect(page.locator('//h2[text()="Customer Login"]')).to_be_visible()
        await expect(page.locator('//h2[text()="Customer Login"]')).to_contain_text('Customer Login')