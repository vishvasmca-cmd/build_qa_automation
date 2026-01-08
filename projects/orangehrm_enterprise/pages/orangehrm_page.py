from playwright.async_api import Page, expect

class OrangehrmPage:
    """
    Admin page for managing system users in OrangeHRM
    URL Pattern: /admin/viewSystemUsers
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_button(self):
        """Button to add a new system user"""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    @property
    def search_button(self):
        """Button to search system users"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def reset_button(self):
        """Button to reset the search filters"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def username_input(self):
        """Input field for username"""
        return self.page.locator('input[placeholder="Username"]').or_(self.page.locator('input[name="username"]'))

    @property
    def user_role_dropdown(self):
        """Dropdown to select user role"""
        return self.page.locator('div:has-text("User Role")').locator('i.oxd-select-text--arrow').or_(self.page.locator('div:has-text("-- Select --")'))

    @property
    def employee_name_input(self):
        """Input field for employee name"""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('input[name="employee_name"]'))

    @property
    def status_dropdown(self):
        """Dropdown to select status"""
        return self.page.locator('div:has-text("Status")').locator('i.oxd-select-text--arrow').or_(self.page.locator('div:has-text("-- Select --")').nth(1))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6:has-text("System Users")')).to_be_visible()
        await expect(page.locator('div:has-text("(10) Records Found")')).to_be_visible()