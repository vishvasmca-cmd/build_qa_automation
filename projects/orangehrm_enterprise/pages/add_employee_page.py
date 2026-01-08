from playwright.async_api import Page, expect

class AddEmployeePage:
    """
    Add Employee page for creating new employee records
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
        return self.page.locator('input[class*="oxd-input oxd-input--active"]').or_(self.page.locator('div:has-text("Employee Id") input'))

    @property
    def save_button(self):
        """Button to save the new employee record"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    @property
    def cancel_button(self):
        """Button to cancel adding a new employee"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.get_by_role('heading', name='Add Employee')).to_be_visible()
        await expect(page).to_have_url(/pim/addEmployee)