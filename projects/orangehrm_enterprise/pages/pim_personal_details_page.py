from playwright.async_api import Page, expect

class PimPersonalDetailsPage:
    """
    PIM Personal Details Page
    URL Pattern: /pim/viewPersonalDetails
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def firstName(self):
        """First Name input field"""
        return self.page.get_by_label('First Name').or_(self.page.locator('input[name="firstName"]'))

    @property
    def middleName(self):
        """Middle Name input field"""
        return self.page.get_by_label('Middle Name').or_(self.page.locator('input[name="middleName"]'))

    @property
    def lastName(self):
        """Last Name input field"""
        return self.page.get_by_label('Last Name').or_(self.page.locator('input[name="lastName"]'))

    @property
    def employeeId(self):
        """Employee ID input field"""
        return self.page.get_by_label('Employee Id').or_(self.page.locator('input[name="employeeId"]'))

    @property
    def otherId(self):
        """Other ID input field"""
        return self.page.get_by_label('Other Id').or_(self.page.locator('input[name="otherId"]'))

    @property
    def driverLicenseNumber(self):
        """Driver's License Number input field"""
        return self.page.get_by_label('Driver's License Number').or_(self.page.locator('input[name="driverLicenseNo"]'))

    @property
    def licenseExpiryDate(self):
        """License Expiry Date input field"""
        return self.page.get_by_label('License Expiry Date').or_(self.page.locator('input[name="licenseExpiryDate"]'))

    @property
    def nationalityDropdown(self):
        """Nationality dropdown"""
        return self.page.get_by_role('combobox', name='Nationality').or_(self.page.locator('div[class*="oxd-select-text--arrow"]'))

    @property
    def maritalStatusDropdown(self):
        """Marital Status dropdown"""
        return self.page.get_by_role('combobox', name='Marital Status').or_(self.page.locator('div[class*="oxd-select-text--arrow"]'))

    @property
    def dateOfBirth(self):
        """Date of Birth input field"""
        return self.page.get_by_label('Date of Birth').or_(self.page.locator('input[placeholder="yyyy-dd-mm"]'))

    @property
    def genderMale(self):
        """Gender Male radio button"""
        return self.page.get_by_label('Male').or_(self.page.locator('input[value="1"]'))

    @property
    def genderFemale(self):
        """Gender Female radio button"""
        return self.page.get_by_label('Female').or_(self.page.locator('input[value="2"]'))

    @property
    def saveButton(self):
        """Save button"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6:has-text("Personal Details")')).to_be_visible()
        await expect(page.locator('//label[text()="Employee Full Name"]')).to_be_visible()