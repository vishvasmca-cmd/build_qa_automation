from playwright.async_api import Page, expect

class HomePage:
    """
    Home page for an automation exercise website. It serves as the entry point, providing information about the site's purpose and navigation to various sections.
    URL Pattern: /
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def signup_login_link(self):
        """Link to the signup or login page."""
        return self.page.get_by_role('link', name='Signup / Login').or_(self.page.locator('a[href="/login"]'))

    @property
    def products_link(self):
        """Link to the products page"""
        return self.page.get_by_role('link', name='Products').or_(self.page.locator('a[href="/products"]'))

    @property
    def test_cases_link(self):
        """Link to the test cases page"""
        return self.page.get_by_role('link', name='Test Cases').or_(self.page.locator('a[href="/test_cases"]'))

    @property
    def api_testing_link(self):
        """Link to the api testing page"""
        return self.page.get_by_role('link', name='API Testing').or_(self.page.locator('a[href="/api_list"]'))

    @property
    def test_cases_button(self):
        """Button to the test cases page"""
        return self.page.get_by_role('button', name='Test Cases').or_(self.page.locator('a[href="/test_cases"]'))

    @property
    def apis_list_for_practice_button(self):
        """Button to the apis list page"""
        return self.page.get_by_role('button', name='APIs list for practice').or_(self.page.locator('a[href="/api_list"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Automation Exercise')
        await expect(page.locator('h2', has_text='Full-Fledged practice website for Automation Engineers')).to_be_visible()
        await expect(page.locator('img[alt="Automation Exercise"]')).to_be_visible()
        await expect(page.url()).to_be('https://automationexercise.com/')