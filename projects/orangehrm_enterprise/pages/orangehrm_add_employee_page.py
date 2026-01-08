from playwright.async_api import Page, expect

class OrangehrmAddEmployeePage:
    """
    Add Employee page for the OrangeHRM application, used to create new employee records.
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_employee_header(self):
        """The main header on the Add Employee page."""
        return self.page.get_by_role('heading', name='Add Employee').or_(self.page.locator('h6.oxd-text.oxd-text--h6.orangehrm-main-title'))

    @property
    def employee_list_link(self):
        """Link to navigate to the employee list page"""
        return self.page.get_by_text('Employee List').or_(self.page.locator('a:has-text("Employee List")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url(/pim/addEmployee)
        await expect(page.get_by_role('heading', name='Add Employee').first()).to_be_visible()