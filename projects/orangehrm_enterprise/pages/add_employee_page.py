from playwright.async_api import Page, expect

class AddEmployeePage:
    """
    Add Employee page for OrangeHRM
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def firstName_input(self):
        """First Name input field"""
        return self.page.get_by_placeholder('First Name').or_(self.page.locator('input[name="firstName"]'))

    @property
    def middleName_input(self):
        """Middle Name input field"""
        return self.page.get_by_placeholder('Middle Name').or_(self.page.locator('input[name="middleName"]'))

    @property
    def lastName_input(self):
        """Last Name input field"""
        return self.page.get_by_placeholder('Last Name').or_(self.page.locator('input[name="lastName"]'))

    @property
    def employeeId_input(self):
        """Employee ID input field"""
        return self.page.locator('input[id="employeeId"]').or_(self.page.get_by_text('Employee Id').locator('xpath=//following-sibling::div/input'))

    @property
    def createLoginDetails_toggle(self):
        """Toggle to create login details for the new employee"""
        return self.page.get_by_role('switch').or_(self.page.locator('.oxd-switch-input'))

    @property
    def save_button(self):
        """Button to save the new employee"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button[type="submit"]'))

    @property
    def cancel_button(self):
        """Button to cancel adding a new employee"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button.oxd-button--ghost'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Add Employee')).to_be_visible()