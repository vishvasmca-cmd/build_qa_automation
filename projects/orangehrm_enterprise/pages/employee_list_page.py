from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List page within the PIM module, allowing users to view, search, and manage employee information.
    URL Pattern: /pim/employees
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def employee_name_input(self):
        """Input field for filtering employees by name."""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]').first)

    @property
    def employee_id_input(self):
        """Input field for filtering employees by ID."""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('div:has-text("Employee Id") input'))

    @property
    def employment_status_dropdown(self):
        """Dropdown to filter employees by employment status."""
        return self.page.locator('div:has-text("Employment Status") div[class*="oxd-select-text--arrow"]').or_(self.page.locator('div:has-text("Employment Status") .oxd-select-text'))

    @property
    def include_dropdown(self):
        """Dropdown to include/exclude current employees."""
        return self.page.locator('div:has-text("Include") div[class*="oxd-select-text--arrow"]').or_(self.page.locator('div:has-text("Include") .oxd-select-text'))

    @property
    def supervisor_name_input(self):
        """Input field to filter employees by supervisor name."""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('div:has-text("Supervisor Name") input'))

    @property
    def job_title_dropdown(self):
        """Dropdown to filter employees by Job Title."""
        return self.page.locator('div:has-text("Job Title") div[class*="oxd-select-text--arrow"]').or_(self.page.locator('div:has-text("Job Title") .oxd-select-text'))

    @property
    def sub_unit_dropdown(self):
        """Dropdown to filter employees by Sub Unit."""
        return self.page.locator('div:has-text("Sub Unit") div[class*="oxd-select-text--arrow"]').or_(self.page.locator('div:has-text("Sub Unit") .oxd-select-text'))

    @property
    def reset_button(self):
        """Button to clear all filter criteria."""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def search_button(self):
        """Button to apply the filter criteria and display matching employees."""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def add_button(self):
        """Button to navigate to the add employee page."""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6', { hasText: 'Employee Information' })).to_be_visible()
        await expect(page.locator('div:has-text("(109) Records Found")')).to_be_visible()