from playwright.async_api import Page, expect

class UnknownPage:
    """
    Page to add a new user in OrangeHRM
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def user_role_dropdown(self):
        """Dropdown to select the user role"""
        return self.page.get_by_text('-- Select --').first.or_(self.page.locator('div[class*="oxd-grid-item"]:nth-child(1) div[class*="oxd-select-text--arrow"]'))

    @property
    def status_dropdown(self):
        """Dropdown to select the user status"""
        return self.page.get_by_text('-- Select --').nth(1).or_(self.page.locator('div[class*="oxd-grid-item"]:nth-child(3) div[class*="oxd-select-text--arrow"]'))

    @property
    def employee_name_input(self):
        """Input field for employee name"""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('input[name="employeeName"]'))

    @property
    def username_input(self):
        """Input field for username"""
        return self.page.locator('input[name="username"]').or_(self.page.locator('div[class*="oxd-grid-item"]:nth-child(4) input'))

    @property
    def password_input(self):
        """Input field for password"""
        return self.page.locator('input[name="password"]').or_(self.page.locator('div[class*="oxd-grid-item"]:nth-child(5) input'))

    @property
    def confirm_password_input(self):
        """Input field to confirm password"""
        return self.page.locator('input[name="confirmPassword"]').or_(self.page.locator('div[class*="oxd-grid-item"]:nth-child(6) input'))

    @property
    def save_button(self):
        """Button to save the new user"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button[type="submit"]'))

    @property
    def cancel_button(self):
        """Button to cancel adding a new user"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button.oxd-button--ghost'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Add User')).to_be_visible()