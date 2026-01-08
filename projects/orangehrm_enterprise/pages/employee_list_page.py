from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List page to view and manage employees
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_employee_button(self):
        """Button to navigate to the Add Employee page"""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    @property
    def employee_name_input(self):
        """Input field for Employee Name"""
        return self.page.locator('input[placeholder="Type for hints..."]').first.or_(self.page.locator('input[placeholder="Type for hints..."]').nth(0))

    @property
    def employee_id_input(self):
        """Input field for Employee ID"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('input[placeholder="Type for hints..."]').nth(1))

    @property
    def employment_status_dropdown(self):
        """Dropdown to select Employment Status"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').first.or_(self.page.locator('div[class*="oxd-select-text--arrow"]').nth(0))

    @property
    def include_dropdown(self):
        """Dropdown to select Include"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(1).or_(self.page.locator('div[class*="oxd-select-text--arrow"]').nth(1))

    @property
    def supervisor_name_input(self):
        """Input field for Supervisor Name"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('input[placeholder="Type for hints..."]').nth(2))

    @property
    def job_title_dropdown(self):
        """Dropdown to select Job Title"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(2).or_(self.page.locator('div[class*="oxd-select-text--arrow"]').nth(2))

    @property
    def sub_unit_dropdown(self):
        """Dropdown to select Sub Unit"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(3).or_(self.page.locator('div[class*="oxd-select-text--arrow"]').nth(3))

    @property
    def reset_button(self):
        """Button to reset the search filters"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def search_button(self):
        """Button to search employees"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6:has-text("Employee Information")')).to_be_visible()
        await expect(page.locator('span:has-text("(104) Records Found")')).to_be_visible()