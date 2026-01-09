from playwright.async_api import Page, expect

class AddEmployeePage:
    """
    Add Employee page
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
        return self.page.locator('input[name="employeeId"]').or_(self.page.locator('div:has-text("Employee Id") input'))

    @property
    def createLoginDetailsToggle(self):
        """Toggle to create login details for the new employee"""
        return self.page.locator('span.oxd-switch-input').or_(self.page.locator('label:has-text("Create Login Details") span.oxd-switch-input'))

    @property
    def saveButton(self):
        """Button to save the new employee"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    @property
    def cancelButton(self):
        """Button to cancel adding a new employee"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button:has-text("Cancel")'))

    @property
    def addProfilePicture(self):
        """Button to add profile picture"""
        return self.page.locator('div.orangehrm-employee-image').or_(self.page.locator('div.orangehrm-employee-image > img'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.get_by_role('heading', name='Add Employee')).to_be_visible()
        await expect(page).to_have_url(/pim/addEmployee)