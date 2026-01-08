from playwright.async_api import Page, expect

class AddEmployeePage:
    """
    Add Employee page for creating new employee records
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def firstName(self):
        """First name input field"""
        return self.page.get_by_placeholder('First Name').or_(self.page.locator('input[name="firstName"]'))

    @property
    def middleName(self):
        """Middle name input field"""
        return self.page.get_by_placeholder('Middle Name').or_(self.page.locator('input[name="middleName"]'))

    @property
    def lastName(self):
        """Last name input field"""
        return self.page.get_by_placeholder('Last Name').or_(self.page.locator('input[name="lastName"]'))

    @property
    def employeeId(self):
        """Employee ID input field"""
        return self.page.locator('input[class*="oxd-input oxd-input--active"]').or_(self.page.locator('div:has-text("Employee Id") input'))

    @property
    def saveButton(self):
        """Save button to submit the form"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    @property
    def cancelButton(self):
        """Cancel button to discard the form"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    @property
    def addProfilePicture(self):
        """Button to upload profile picture"""
        return self.page.locator('div.orangehrm-employee-image > div > input[type="file"]').or_(self.page.locator('div.orangehrm-employee-image > div > div'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Add Employee')).to_be_visible()
        await expect(page.locator('input[name="firstName"]')).to_be_visible()
        await expect(page.locator('input[name="employeeId"]')).to_be_visible()