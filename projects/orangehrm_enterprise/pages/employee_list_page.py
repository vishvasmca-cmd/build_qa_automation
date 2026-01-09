from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List page in OrangeHRM
    URL Pattern: /pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Employee Name Input(self):
        """Input field for Employee Name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]').first)

    @property
    def Employee Id Input(self):
        """Input field for Employee ID"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('div.oxd-input-group').nth(1) input)

    @property
    def Employment Status Dropdown(self):
        """Dropdown for selecting Employment Status"""
        return self.page.locator('div.oxd-select-text--after i').or_(self.page.locator('div.oxd-input-group').nth(2) div[class="oxd-select-text oxd-select-text--active"])

    @property
    def Include Dropdown(self):
        """Dropdown for selecting Include options"""
        return self.page.locator('div.oxd-select-text--after i').nth(1).or_(self.page.locator('div.oxd-input-group').nth(3) div[class="oxd-select-text oxd-select-text--active"])

    @property
    def Supervisor Name Input(self):
        """Input field for Supervisor Name"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('div.oxd-input-group').nth(4) input)

    @property
    def Job Title Dropdown(self):
        """Dropdown for selecting Job Title"""
        return self.page.locator('div.oxd-select-text--after i').nth(2).or_(self.page.locator('div.oxd-input-group').nth(5) div[class="oxd-select-text oxd-select-text--active"])

    @property
    def Sub Unit Dropdown(self):
        """Dropdown for selecting Sub Unit"""
        return self.page.locator('div.oxd-select-text--after i').nth(3).or_(self.page.locator('div.oxd-input-group').nth(6) div[class="oxd-select-text oxd-select-text--active"])

    @property
    def Reset Button(self):
        """Button to reset the search filters"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button.oxd-button--ghost'))

    @property
    def Search Button(self):
        """Button to initiate the employee search"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button.oxd-button--secondary'))

    @property
    def Add Button(self):
        """Button to add a new employee"""
        return self.page.get_by_role('button', name='Add').or_(self.page.locator('button.oxd-button--success'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url(/pim/viewEmployeeList)
        await expect(page.locator('div.orangehrm-header-container h6').first).to_have_text('Employee Information')
        await expect(page.locator('div.orangehrm-paper-container span.oxd-text').first).to_contain_text('Records Found')