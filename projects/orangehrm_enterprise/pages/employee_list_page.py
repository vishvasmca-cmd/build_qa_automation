from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List Page
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Employee Name Input(self):
        """Input field for employee name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]'))

    @property
    def Employee ID Input(self):
        """Input field for employee ID"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('div:has-text("Employee Id") input'))

    @property
    def Employment Status Dropdown(self):
        """Dropdown for selecting employment status"""
        return self.page.locator('div:has-text("Employment Status") div[class*="select-wrapper"]').or_(self.page.locator('div:has-text("Employment Status") .oxd-select-text'))

    @property
    def Include Dropdown(self):
        """Dropdown for selecting include options"""
        return self.page.locator('div:has-text("Include") div[class*="select-wrapper"]').or_(self.page.locator('div:has-text("Include") .oxd-select-text'))

    @property
    def Supervisor Name Input(self):
        """Input field for supervisor name"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('div:has-text("Supervisor Name") input'))

    @property
    def Job Title Dropdown(self):
        """Dropdown for selecting job title"""
        return self.page.locator('div:has-text("Job Title") div[class*="select-wrapper"]').or_(self.page.locator('div:has-text("Job Title") .oxd-select-text'))

    @property
    def Sub Unit Dropdown(self):
        """Dropdown for selecting sub unit"""
        return self.page.locator('div:has-text("Sub Unit") div[class*="select-wrapper"]').or_(self.page.locator('div:has-text("Sub Unit") .oxd-select-text'))

    @property
    def Reset Button(self):
        """Button to reset the search form"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def Search Button(self):
        """Button to search for employees"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def Add Button(self):
        """Button to add a new employee"""
        return self.page.get_by_role('button', name='Add').or_(self.page.locator('button:has-text(" Add ")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6:has-text("Employee Information")')).to_be_visible()
        await expect(page.locator('div:has-text("(102) Records Found")')).to_be_visible()