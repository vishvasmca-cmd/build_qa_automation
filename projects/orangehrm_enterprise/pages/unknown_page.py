from playwright.async_api import Page, expect

class UnknownPage:
    """
    Page to add a new user in the OrangeHRM system.
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def user_role_dropdown(self):
        """Dropdown to select the user role (Admin/ESS)."""
        return self.page.get_by_role('combobox', name='User Role*').or_(self.page.locator('div[class*="oxd-grid-item"]:nth-child(1) div[class*="oxd-select-wrapper"]'))

    @property
    def employee_name_input(self):
        """Input field to enter the employee's name."""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]'))

    @property
    def status_dropdown(self):
        """Dropdown to select the user's status (Enabled/Disabled)."""
        return self.page.get_by_role('combobox', name='Status*').or_(self.page.locator('div[class*="oxd-grid-item"]:nth-child(3) div[class*="oxd-select-wrapper"]'))

    @property
    def username_input(self):
        """Input field for the username."""
        return self.page.get_by_label('Username*').or_(self.page.locator('label:has-text("Username") + input'))

    @property
    def password_input(self):
        """Input field for the password."""
        return self.page.get_by_label('Password*').or_(self.page.locator('label:has-text("Password") + input'))

    @property
    def confirm_password_input(self):
        """Input field to confirm the password."""
        return self.page.get_by_label('Confirm Password*').or_(self.page.locator('label:has-text("Confirm Password") + input'))

    @property
    def save_button(self):
        """Button to save the new user."""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    @property
    def cancel_button(self):
        """Button to cancel the creation of a new user."""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Add User')).to_be_visible()