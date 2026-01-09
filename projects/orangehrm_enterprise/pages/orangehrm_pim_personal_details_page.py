from playwright.async_api import Page, expect

class OrangehrmPimPersonalDetailsPage:
    """
    PIM Personal Details Page
    URL Pattern: /pim/viewPersonalDetails/empNumber/*
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
    def nickname_input(self):
        """Nickname input field"""
        return self.page.get_by_label('Nickname').or_(self.page.locator('input[name="nickName"]'))

    @property
    def employeeId_input(self):
        """Employee ID input field"""
        return self.page.get_by_label('Employee Id').or_(self.page.locator('input[name="employeeId"]'))

    @property
    def nationality_dropdown(self):
        """Nationality dropdown"""
        return self.page.get_by_role('combobox', name='Nationality').or_(self.page.locator('div[class*="oxd-select-text--arrow"]'))

    @property
    def maritalStatus_dropdown(self):
        """Marital Status dropdown"""
        return self.page.get_by_role('combobox', name='Marital Status').or_(self.page.locator('div[class*="oxd-select-text--arrow"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('//h6[text()="Personal Details"]')).to_be_visible()