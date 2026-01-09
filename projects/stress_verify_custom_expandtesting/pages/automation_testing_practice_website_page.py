from playwright.async_api import Page, expect

class AutomationTestingPracticeWebsitePage:
    """
    Home page for Automation Testing Practice Website
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to search for examples"""
        return self.page.get_by_placeholder('Search an example...').or_(self.page.locator('input[placeholder="Search an example..."]'))

    @property
    def search_button(self):
        """Button to submit the search query"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def web_inputs_link(self):
        """Link to the Web Inputs page"""
        return self.page.get_by_text('Web inputs').or_(self.page.locator('div:has-text("Web inputs") a'))

    @property
    def test_login_page_link(self):
        """Link to the Test Login Page"""
        return self.page.get_by_text('Test Login Page').or_(self.page.locator('div:has-text("Test Login Page") a'))

    @property
    def test_register_page_link(self):
        """Link to the Test Register Page"""
        return self.page.get_by_text('Test Register Page').or_(self.page.locator('div:has-text("Test Register Page") a'))

    @property
    def forgot_password_form_link(self):
        """Link to the Forgot Password Form"""
        return self.page.get_by_text('Forgot Password Form').or_(self.page.locator('div:has-text("Forgot Password Form") a'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Automation Testing Practice WebSite for QA and Developers')
        await expect(page.get_by_text('Automation Testing Practice WebSite for QA and Developers')).to_be_visible()
        await expect(page.locator('text=Sample applications for practice test automation')).to_be_visible()