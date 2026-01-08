from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List Page to view and manage employee information
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def employee_name_input(self):
        """Input field for Employee Name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]'))

    @property
    def employee_id_input(self):
        """Input field for Employee ID"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('input[class*="oxd-input"]').nth(3))

    @property
    def employment_status_dropdown(self):
        """Dropdown for selecting Employment Status"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').or_(self.page.locator('div[class*="oxd-select-text--arrow"]').nth(0))

    @property
    def include_dropdown(self):
        """Dropdown for selecting Include options"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(1).or_(self.page.locator('div[class*="oxd-select-text--arrow"]'))

    @property
    def supervisor_name_input(self):
        """Input field for Supervisor Name"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('input[class*="oxd-input"]').nth(5))

    @property
    def job_title_dropdown(self):
        """Dropdown for selecting Job Title"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(2).or_(self.page.locator('div[class*="oxd-select-text--arrow"]'))

    @property
    def sub_unit_dropdown(self):
        """Dropdown for selecting Sub Unit"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').nth(3).or_(self.page.locator('div[class*="oxd-select-text--arrow"]'))

    @property
    def reset_button(self):
        """Button to reset the search filters"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def search_button(self):
        """Button to search employees based on filters"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def add_button(self):
        """Button to add a new employee"""
        return self.page.get_by_role('button', name=' Add').or_(self.page.locator('button:has-text(" Add")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6:has-text("Employee Information")')).to_be_visible()
        await expect(page.locator('//span[text()="PIM"]')).to_be_visible()