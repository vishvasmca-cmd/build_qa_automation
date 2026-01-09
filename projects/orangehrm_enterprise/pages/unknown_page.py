from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page is used to add a new user to the OrangeHRM system.
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def user_role_dropdown(self):
        """Dropdown to select the user role (Admin or ESS)."""
        return self.page.get_by_text('-- Select --').first.or_(self.page.locator('div').filter(has_text='User Role').locator('i'))

    @property
    def employee_name_input(self):
        """Input field to enter the employee's name."""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('div').filter(has_text='Employee Name').locator('input'))

    @property
    def status_dropdown(self):
        """Dropdown to select the user's status (Enabled or Disabled)."""
        return self.page.get_by_text('-- Select --').nth(1).or_(self.page.locator('div').filter(has_text='Status').locator('i'))

    @property
    def username_input(self):
        """Input field to enter the username."""
        return self.page.locator('input[placeholder="Type for username"]').or_(self.page.locator('div').filter(has_text='Username').locator('input'))

    @property
    def password_input(self):
        """Input field to enter the password."""
        return self.page.locator('input[type="password"]').first.or_(self.page.locator('div').filter(has_text='Password').locator('input'))

    @property
    def confirm_password_input(self):
        """Input field to confirm the password."""
        return self.page.locator('input[type="password"]').nth(1).or_(self.page.locator('div').filter(has_text='Confirm Password').locator('input'))

    @property
    def save_button(self):
        """Button to save the new user."""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button.oxd-button--secondary.oxd-button--success'))

    @property
    def cancel_button(self):
        """Button to cancel adding the new user."""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button.oxd-button--text.oxd-button--danger'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Add User')).to_be_visible()