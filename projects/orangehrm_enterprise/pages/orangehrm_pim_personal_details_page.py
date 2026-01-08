from playwright.async_api import Page, expect

class OrangehrmPimPersonalDetailsPage:
    """
    PIM Personal Details Page
    URL Pattern: /pim/viewPersonalDetails
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def firstName_input(self):
        """First Name input field"""
        return self.page.get_by_label('First Name').or_(self.page.locator('input[name="firstName"]'))

    @property
    def middleName_input(self):
        """Middle Name input field"""
        return self.page.get_by_label('Middle Name').or_(self.page.locator('input[name="middleName"]'))

    @property
    def lastName_input(self):
        """Last Name input field"""
        return self.page.get_by_label('Last Name').or_(self.page.locator('input[name="lastName"]'))

    @property
    def employeeId_input(self):
        """Employee ID input field"""
        return self.page.get_by_label('Employee Id').or_(self.page.locator('input[name="employeeId"]'))

    @property
    def nationality_dropdown(self):
        """Nationality dropdown"""
        return self.page.get_by_role('combobox', name='Nationality').or_(self.page.locator('div:has-text("Nationality") >> div >> div.oxd-select-text--after'))

    @property
    def maritalStatus_dropdown(self):
        """Marital Status dropdown"""
        return self.page.get_by_role('combobox', name='Marital Status').or_(self.page.locator('div:has-text("Marital Status") >> div >> div.oxd-select-text--after'))

    @property
    def save_button(self):
        """Save button"""
        return self.page.get_by_role('button', name='Save').or_(self.page.locator('button:has-text("Save")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6:has-text("Personal Details")')).to_be_visible()