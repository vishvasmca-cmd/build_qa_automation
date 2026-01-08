from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    Employee List Page for managing employee information
    URL Pattern: /pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def employee_name_input(self):
        """Input field for Employee Name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]:nth-of-type(1)'))

    @property
    def employee_id_input(self):
        """Input field for Employee ID"""
        return self.page.locator('input[placeholder="Type for hints..."]:nth-of-type(2)').or_(self.page.locator('input[class*="oxd-input"]').nth(2))

    @property
    def employment_status_dropdown(self):
        """Dropdown for selecting Employment Status"""
        return self.page.locator('div[class*="oxd-select-text"]').nth(1).or_(self.page.locator('div[class*="oxd-select-text"]:has-text("-- Select --")'))

    @property
    def include_dropdown(self):
        """Dropdown for selecting employee inclusion criteria"""
        return self.page.locator('div[class*="oxd-select-text"]').nth(2).or_(self.page.locator('div[class*="oxd-select-text"]:has-text("Current Employees Only")'))

    @property
    def supervisor_name_input(self):
        """Input field for Supervisor Name"""
        return self.page.locator('input[placeholder="Type for hints..."]:nth-of-type(3)').or_(self.page.locator('input[class*="oxd-input"]').nth(3))

    @property
    def job_title_dropdown(self):
        """Dropdown for selecting Job Title"""
        return self.page.locator('div[class*="oxd-select-text"]').nth(3).or_(self.page.locator('div[class*="oxd-select-text"]:has-text("-- Select --")').nth(1))

    @property
    def sub_unit_dropdown(self):
        """Dropdown for selecting Sub Unit"""
        return self.page.locator('div[class*="oxd-select-text"]').nth(4).or_(self.page.locator('div[class*="oxd-select-text"]:has-text("-- Select --")').nth(2))

    @property
    def reset_button(self):
        """Button to reset the search filters"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def search_button(self):
        """Button to initiate the employee search"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def add_button(self):
        """Button to add a new employee"""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url(/pim/viewEmployeeList)
        await expect(page.locator('div[class*="oxd-topbar-header-breadcrumb"]').get_by_text('Employee List')).to_be_visible()
        await expect(page.locator('div[class*="oxd-table-filter-header"]').get_by_text('Employee Information')).to_be_visible()