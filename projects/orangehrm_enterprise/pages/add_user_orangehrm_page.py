from playwright.async_api import Page, expect

class AddUserOrangehrmPage:
    """
    Add User page in OrangeHRM
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def user_role_dropdown(self):
        """Dropdown to select User Role"""
        return self.page.get_by_role('combobox', name='User Role').or_(self.page.locator('div:has-text("User Role")').locator('div > div.oxd-select-text--arrow'))

    @property
    def employee_name_input(self):
        """Input field for Employee Name"""
        return self.page.get_by_label('Employee Name').or_(self.page.locator('input[placeholder="Type for hints..."]'))

    @property
    def status_dropdown(self):
        """Dropdown to select Status"""
        return self.page.get_by_role('combobox', name='Status').or_(self.page.locator('div:has-text("Status")').locator('div > div.oxd-select-text--arrow'))

    @property
    def username_input(self):
        """Input field for Username"""
        return self.page.get_by_label('Username').or_(self.page.locator('input[name="username"]'))

    @property
    def password_input(self):
        """Input field for Password"""
        return self.page.get_by_label('Password').or_(self.page.locator('input[name="password"]'))

    @property
    def confirm_password_input(self):
        """Input field for Confirm Password"""
        return self.page.get_by_label('Confirm Password').or_(self.page.locator('input[name="confirmPassword"]'))

    @property
    def save_button(self):
        """Button to save the new user"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button.oxd-button--secondary.oxd-button--success'))

    @property
    def cancel_button(self):
        """Button to cancel the new user creation"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button.oxd-button--text.oxd-button--danger'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.locator('h6', { hasText: 'Add User' })).to_be_visible()
        await expect(page).to_have_url(/admin/saveSystemUser)