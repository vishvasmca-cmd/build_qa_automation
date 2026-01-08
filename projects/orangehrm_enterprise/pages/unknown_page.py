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
        """Dropdown to select the user role."""
        return self.page.get_by_text('-- Select --').first.or_(self.page.locator('div:has-text("User Role") >> div >> div.oxd-select-text--after'))

    @property
    def employee_name_input(self):
        """Input field for entering the employee name."""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('div:has-text("Employee Name") >> input'))

    @property
    def username_input(self):
        """Input field for entering the username."""
        return self.page.locator('div:has-text("Username") >> input').or_(self.page.locator('input[name="username"]'))

    @property
    def status_dropdown(self):
        """Dropdown to select the user status."""
        return self.page.get_by_text('-- Select --').nth(1).or_(self.page.locator('div:has-text("Status") >> div >> div.oxd-select-text--after'))

    @property
    def password_input(self):
        """Input field for entering the password."""
        return self.page.locator('div:has-text("Password") >> input').or_(self.page.locator('input[name="password"]'))

    @property
    def confirm_password_input(self):
        """Input field for confirming the password."""
        return self.page.locator('div:has-text("Confirm Password") >> input').or_(self.page.locator('input[name="confirmPassword"]'))

    @property
    def save_button(self):
        """Button to save the new user."""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    @property
    def cancel_button(self):
        """Button to cancel the new user creation."""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.get_by_role('heading', name='Add User')).to_be_visible()
        await expect(page).to_have_url(/admin/saveSystemUser)