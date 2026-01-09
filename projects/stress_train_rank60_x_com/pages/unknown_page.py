from playwright.async_api import Page, expect

class UnknownPage:
    """
    Landing/Signup page for X (formerly Twitter)
    URL Pattern: https://x.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def sign_up_with_google_button(self):
        """Button to sign up using Google account"""
        return self.page.get_by_role('button', name='Sign up with Google').or_(self.page.locator('div:has-text("Sign up with Google")'))

    @property
    def sign_up_with_apple_button(self):
        """Button to sign up using Apple account"""
        return self.page.get_by_role('button', name='Sign up with Apple').or_(self.page.locator('div:has-text("Sign up with Apple")'))

    @property
    def create_account_button(self):
        """Button to create a new account"""
        return self.page.get_by_role('button', name='Create account').or_(self.page.locator('div:has-text("Create account")'))

    @property
    def sign_in_link(self):
        """Link to sign into an existing account"""
        return self.page.get_by_role('link', name='Sign in').or_(self.page.locator('div:has-text("Sign in")'))

    @property
    def get_grok_link(self):
        """Link to Get Grok"""
        return self.page.get_by_role('link', name='Get Grok').or_(self.page.locator('div:has-text("Get Grok")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('X')
        await expect(page.locator('h1:has-text("Happening now")')).to_be_visible()
        await expect(page.locator('h2:has-text("Join today.")')).to_be_visible()