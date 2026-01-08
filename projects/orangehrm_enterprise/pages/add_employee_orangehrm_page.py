from playwright.async_api import Page, expect

class AddEmployeeOrangehrmPage:
    """
    Add Employee page in OrangeHRM
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name_input(self):
        """Input field for the employee's first name"""
        return self.page.get_by_placeholder('First Name').or_(self.page.locator('input[name="firstName"]'))

    @property
    def middle_name_input(self):
        """Input field for the employee's middle name"""
        return self.page.get_by_placeholder('Middle Name').or_(self.page.locator('input[name="middleName"]'))

    @property
    def last_name_input(self):
        """Input field for the employee's last name"""
        return self.page.get_by_placeholder('Last Name').or_(self.page.locator('input[name="lastName"]'))

    @property
    def employee_id_input(self):
        """Input field for the employee's ID"""
        return self.page.get_by_label('Employee Id').or_(self.page.locator('input[class*="oxd-input oxd-input--active"][id]'))

    @property
    def create_login_details_toggle(self):
        """Toggle to enable/disable creating login details for the employee"""
        return self.page.get_by_role('switch').or_(self.page.locator('.oxd-switch-input'))

    @property
    def save_button(self):
        """Button to save the new employee"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    @property
    def cancel_button(self):
        """Button to cancel adding a new employee"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    @property
    def add_profile_picture(self):
        """Button to add profile picture"""
        return self.page.locator('div.orangehrm-employee-image > div > input[type="file"]').or_(self.page.locator('div.orangehrm-employee-image > div > i'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.get_by_role('heading', name='Add Employee')).to_be_visible()
        await expect(page).to_have_url(/pim/addEmployee)