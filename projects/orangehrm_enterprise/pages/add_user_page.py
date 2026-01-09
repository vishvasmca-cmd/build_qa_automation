from playwright.async_api import Page, expect

class AddUserPage:
    """
    Add User page in OrangeHRM
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def user_role_dropdown(self):
        """Dropdown to select the user role"""
        return self.page.get_by_text('-- Select --').first.or_(self.page.locator('div:has-text("User Role")').locator('i'))

    @property
    def employee_name_input(self):
        """Input field for the employee name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('label:has-text("Employee Name") + div > input'))

    @property
    def status_dropdown(self):
        """Dropdown to select the status of the user"""
        return self.page.get_by_text('-- Select --').nth(1).or_(self.page.locator('div:has-text("Status")').locator('i'))

    @property
    def username_input(self):
        """Input field for the username"""
        return self.page.locator('label:has-text("Username") + div > input').or_(self.page.get_by_text('Username *'))

    @property
    def password_input(self):
        """Input field for the password"""
        return self.page.locator('label:has-text("Password") + div > input').or_(self.page.get_by_text('Password *'))

    @property
    def confirm_password_input(self):
        """Input field to confirm the password"""
        return self.page.locator('label:has-text("Confirm Password") + div > input').or_(self.page.get_by_text('Confirm Password *'))

    @property
    def cancel_button(self):
        """Button to cancel adding the user"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    @property
    def save_button(self):
        """Button to save the new user"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.get_by_role('heading', name='Add User')).to_be_visible()
        await expect(page).to_have_url(/admin/saveSystemUser)