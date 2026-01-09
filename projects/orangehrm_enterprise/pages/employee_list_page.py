from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List Page in OrangeHRM
    URL Pattern: /pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Employee Name Input(self):
        """Input field for filtering by employee name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]').first)

    @property
    def Employee Id Input(self):
        """Input field for filtering by employee id"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('Employee Id').locator('xpath=//following-sibling::input'))

    @property
    def Employment Status Dropdown(self):
        """Dropdown for filtering by employment status"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(0).or_(self.page.locator('Employment Status').locator('xpath=//following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def Include Dropdown(self):
        """Dropdown for filtering by include"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(1).or_(self.page.locator('Include').locator('xpath=//following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def Supervisor Name Input(self):
        """Input field for filtering by supervisor name"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('Supervisor Name').locator('xpath=//following-sibling::input'))

    @property
    def Job Title Dropdown(self):
        """Dropdown for filtering by job title"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(2).or_(self.page.locator('Job Title').locator('xpath=//following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def Sub Unit Dropdown(self):
        """Dropdown for filtering by sub unit"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(3).or_(self.page.locator('Sub Unit').locator('xpath=//following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def Reset Button(self):
        """Button to reset the filter form"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def Search Button(self):
        """Button to submit the filter form"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def Add Button(self):
        """Button to add a new employee"""
        return self.page.get_by_role('button', name=' Add').or_(self.page.locator('button:has-text(" Add")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url('https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList')
        await expect(page.locator('h6', has_text='Employee Information')).to_be_visible()
        await expect(page.locator('div[class="oxd-table-body"]')).to_be_visible()