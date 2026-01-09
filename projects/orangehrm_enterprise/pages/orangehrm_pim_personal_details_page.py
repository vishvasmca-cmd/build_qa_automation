from playwright.async_api import Page, expect

class OrangehrmPimPersonalDetailsPage:
    """
    This page allows users to view and modify the personal details of an employee within the OrangeHRM system.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def FirstName Field(self):
        """Input field for the employee's first name."""
        return self.page.//label[text()='First Name']/following::input.or_(self.page.input[name='firstName'])

    @property
    def MiddleName Field(self):
        """Input field for the employee's middle name."""
        return self.page.//label[text()='Middle Name']/following::input.or_(self.page.input[name='middleName'])

    @property
    def LastName Field(self):
        """Input field for the employee's last name."""
        return self.page.//label[text()='Last Name']/following::input.or_(self.page.input[name='lastName'])

    @property
    def Employee Id Field(self):
        """Input field for the employee's ID."""
        return self.page.//label[text()='Employee Id']/following::input.or_(self.page.input[name='employeeId'])

    @property
    def Other Id Field(self):
        """Input field for the employee's other ID."""
        return self.page.//label[text()='Other Id']/following::input.or_(self.page.input[name='otherId'])

    @property
    def Driver's License Number Field(self):
        """Input field for the employee's driver's license number."""
        return self.page.//label[text()="Driver's License Number"]/following::input.or_(self.page.input[name='driverLicenseNo'])

    @property
    def License Expiry Date Field(self):
        """Input field for the employee's license expiry date."""
        return self.page.//label[text()='License Expiry Date']/following::input.or_(self.page.input[name='licenseExpiryDate'])

    @property
    def Nationality Dropdown(self):
        """Dropdown for selecting the employee's nationality."""
        return self.page.//label[text()='Nationality']/following::div[@class='oxd-select-text--after'].or_(self.page.div[class='oxd-select-text--after'])

    @property
    def Marital Status Dropdown(self):
        """Dropdown for selecting the employee's marital status."""
        return self.page.//label[text()='Marital Status']/following::div[@class='oxd-select-text--after'].or_(self.page.div[class='oxd-select-text--after'])

    @property
    def Date of Birth Field(self):
        """Input field for the employee's date of birth."""
        return self.page.//label[text()='Date of Birth']/following::input.or_(self.page.input[name='dateOfBirth'])

    @property
    def Gender Male Radio Button(self):
        """Radio button for selecting the employee's gender as male."""
        return self.page.//label[text()='Male']/preceding-sibling::input.or_(self.page.input[value='1'])

    @property
    def Gender Female Radio Button(self):
        """Radio button for selecting the employee's gender as female."""
        return self.page.//label[text()='Female']/preceding-sibling::input.or_(self.page.input[value='2'])

    @property
    def Save Button(self):
        """Button to save the personal details."""
        return self.page.//button[text()=' Save '].or_(self.page.button[type='submit'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Assert that the page title contains 'OrangeHRM'
        await Assert that the 'Personal Details' header is displayed
        await Assert that the 'First Name' field is present
        await Assert that the 'Save' button is present