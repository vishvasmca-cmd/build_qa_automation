from playwright.async_api import Page, expect

class UnknownPage:
    """
    Add User page in OrangeHRM
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def user_role_dropdown(self):
        """Dropdown to select the user role"""
        return self.page.get_by_text('-- Select --').first.or_(self.page.locator('div').filter(has_text='User Role').locator('i'))

    @property
    def employee_name_input(self):
        """Input field for employee name"""
        return self.page.get_by_label('Employee Name*').or_(self.page.locator('input[name="employeeName"]'))

    @property
    def status_dropdown(self):
        """Dropdown to select the status"""
        return self.page.get_by_text('-- Select --').nth(1).or_(self.page.locator('div').filter(has_text='Status').locator('i'))

    @property
    def username_input(self):
        """Input field for username"""
        return self.page.get_by_label('Username*').or_(self.page.locator('input[name="username"]'))

    @property
    def password_input(self):
        """Input field for password"""
        return self.page.get_by_label('Password*').or_(self.page.locator('input[name="password"]'))

    @property
    def confirm_password_input(self):
        """Input field to confirm password"""
        return self.page.get_by_label('Confirm Password*').or_(self.page.locator('input[name="confirmPassword"]'))

    @property
    def cancel_button(self):
        """Button to cancel adding a user"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    @property
    def save_button(self):
        """Button to save the new user"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Add User')).to_be_visible()