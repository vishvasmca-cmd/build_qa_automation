from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List page in OrangeHRM
    URL Pattern: /pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_employee_button(self):
        """Button to navigate to the Add Employee page"""
        return self.page.get_by_role('button', name=' Add').or_(self.page.locator('button:has-text(" Add")'))

    @property
    def employee_name_input(self):
        """Input field for filtering employees by name"""
        return self.page.locator('input[placeholder="Type for hints..."]').first.or_(self.page.locator('div:has-text("Employee Name") input'))

    @property
    def employee_id_input(self):
        """Input field for filtering employees by employee ID"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('div:has-text("Employee Id") input'))

    @property
    def employment_status_dropdown(self):
        """Dropdown for filtering employees by employment status"""
        return self.page.locator('div:has-text("Employment Status") div[class*="oxd-select-text"]').or_(self.page.locator('div:has-text("Employment Status") .oxd-select-text'))

    @property
    def include_dropdown(self):
        """Dropdown for filtering employees by inclusion criteria"""
        return self.page.locator('div:has-text("Include") div[class*="oxd-select-text"]').or_(self.page.locator('div:has-text("Include") .oxd-select-text'))

    @property
    def search_button(self):
        """Button to apply the filter criteria"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def reset_button(self):
        """Button to reset the filter criteria"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6').first).to_have_text('Employee Information')
        await expect(page.locator('//div[@class="oxd-table-body"]/div').count()).toBeGreaterThan(0)