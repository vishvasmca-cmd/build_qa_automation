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
        return self.page.get_by_label('User Role*').or_(self.page.locator('//label[text()="User Role*"]/following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def employee_name_input(self):
        """Input field to enter the employee name"""
        return self.page.get_by_label('Employee Name*').or_(self.page.locator('input[placeholder="Type for hints..."]'))

    @property
    def status_dropdown(self):
        """Dropdown to select the status of the user"""
        return self.page.get_by_label('Status*').or_(self.page.locator('//label[text()="Status*"]/following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def password_input(self):
        """Input field to enter the password"""
        return self.page.get_by_label('Password*').or_(self.page.locator('input[type="password"]').nth(0))

    @property
    def confirm_password_input(self):
        """Input field to confirm the password"""
        return self.page.get_by_label('Confirm Password*').or_(self.page.locator('input[type="password"]').nth(1))

    @property
    def save_button(self):
        """Button to save the new user"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button.oxd-button--secondary.oxd-button--success'))

    @property
    def cancel_button(self):
        """Button to cancel adding the new user"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button.oxd-button--label-warn'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.get_by_text('Add User')).to_be_visible()
        await expect(page).to_have_url(/admin/saveSystemUser)