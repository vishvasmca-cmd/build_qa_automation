from playwright.async_api import Page, expect

class OrangehrmAddEmployeePage:
    """
    Add Employee page in OrangeHRM
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def firstName(self):
        """First Name input field"""
        return self.page.locator('input[name="firstName"]').or_(self.page.locator('input[placeholder="First Name"]'))

    @property
    def middleName(self):
        """Middle Name input field"""
        return self.page.locator('input[name="middleName"]').or_(self.page.locator('input[placeholder="Middle Name"]'))

    @property
    def lastName(self):
        """Last Name input field"""
        return self.page.locator('input[name="lastName"]').or_(self.page.locator('input[placeholder="Last Name"]'))

    @property
    def employeeId(self):
        """Employee ID input field"""
        return self.page.locator('input[name="employeeId"]').or_(self.page.locator('input[class="oxd-input oxd-input--active"]'))

    @property
    def createLoginDetailsToggle(self):
        """Toggle to create login details"""
        return self.page.locator('span.oxd-switch-input').or_(self.page.locator('label[class="oxd-switch-wrapper"]'))

    @property
    def saveButton(self):
        """Save button to submit the form"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button[type="submit"]'))

    @property
    def cancelButton(self):
        """Cancel button to clear the form"""
        return self.page.get_by_role('button', name='Cancel').or_(self.page.locator('button.oxd-button--ghost'))

    @property
    def addProfilePicture(self):
        """Button to add profile picture"""
        return self.page.locator('div.orangehrm-employee-image').or_(self.page.locator('div.oxd-file-div'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url('https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee')
        await expect(page.get_by_role('heading', name='Add Employee')).to_be_visible()