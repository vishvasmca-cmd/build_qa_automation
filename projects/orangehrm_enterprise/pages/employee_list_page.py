from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List page to view and manage employee information
    URL Pattern: /pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_employee_button(self):
        """Button to navigate to the Add Employee page"""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    @property
    def search_button(self):
        """Button to filter employee list based on search criteria"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def reset_button(self):
        """Button to clear the search criteria"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def employee_name_input(self):
        """Input field to enter employee name for filtering"""
        return self.page.locator('input[placeholder="Type for hints..."]').first.or_(self.page.locator('div:has-text("Employee Name") input'))

    @property
    def employee_id_input(self):
        """Input field to enter employee id for filtering"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('div:has-text("Employee Id") input'))

    @property
    def employment_status_dropdown(self):
        """Dropdown to select employment status for filtering"""
        return self.page.locator('div:has-text("Employment Status") div[role="combobox"]').or_(self.page.locator('div:has-text("Employment Status") .oxd-select-text'))

    @property
    def include_dropdown(self):
        """Dropdown to select include status for filtering"""
        return self.page.locator('div:has-text("Include") div[role="combobox"]').or_(self.page.locator('div:has-text("Include") .oxd-select-text'))

    @property
    def supervisor_name_input(self):
        """Input field to enter supervisor name for filtering"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('div:has-text("Supervisor Name") input'))

    @property
    def job_title_dropdown(self):
        """Dropdown to select job title for filtering"""
        return self.page.locator('div:has-text("Job Title") div[role="combobox"]').or_(self.page.locator('div:has-text("Job Title") .oxd-select-text'))

    @property
    def sub_unit_dropdown(self):
        """Dropdown to select sub unit for filtering"""
        return self.page.locator('div:has-text("Sub Unit") div[role="combobox"]').or_(self.page.locator('div:has-text("Sub Unit") .oxd-select-text'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6', has_text='Employee Information')).to_be_visible()
        await expect(page.locator('div:has-text("(120) Records Found")')).to_be_visible()