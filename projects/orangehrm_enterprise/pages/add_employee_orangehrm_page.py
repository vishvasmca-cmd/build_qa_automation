from playwright.async_api import Page, expect

class AddEmployeeOrangehrmPage:
    """
    This page is used to add a new employee to the OrangeHRM system.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def First Name(self):
        """Input field for the employee's first name."""
        return self.page.[name='firstName'].or_(self.page.input[placeholder='First Name'])

    @property
    def Middle Name(self):
        """Input field for the employee's middle name."""
        return self.page.[name='middleName'].or_(self.page.input[placeholder='Middle Name'])

    @property
    def Last Name(self):
        """Input field for the employee's last name."""
        return self.page.[name='lastName'].or_(self.page.input[placeholder='Last Name'])

    @property
    def Employee Id(self):
        """Input field for the employee's ID."""
        return self.page.[name='employeeId'].or_(self.page.div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > input)

    @property
    def Create Login Details Toggle(self):
        """Toggle to enable or disable creating login details for the new employee."""
        return self.page.oxd-switch-input.or_(self.page.span.oxd-switch-input)

    @property
    def Save Button(self):
        """Button to save the new employee's information."""
        return self.page.button:has-text('Save').or_(self.page.button.oxd-button--secondary)

    @property
    def Cancel Button(self):
        """Button to cancel adding a new employee."""
        return self.page.button:has-text('Cancel').or_(self.page.button.oxd-button--ghost)

    @property
    def Add Profile Picture(self):
        """Button to upload a profile picture for the employee."""
        return self.page.div.orangehrm-employee-image > div > input[type=file].or_(self.page.div.orangehrm-employee-image > div > input)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Assert that the page title is 'OrangeHRM'
        await Assert that the header text is 'Add Employee'
        await Assert that the 'First Name' field is present
        await Assert that the 'Last Name' field is present
        await Assert that the 'Save' button is present