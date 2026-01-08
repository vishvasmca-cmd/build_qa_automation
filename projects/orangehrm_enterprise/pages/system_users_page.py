from playwright.async_api import Page, expect

class SystemUsersPage:
    """
    System Users page to manage user accounts
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_button(self):
        """Button to add a new system user"""
        return self.page.get_by_role('button', name='Add').or_(self.page.locator('button:has-text("Add")'))

    @property
    def username_filter(self):
        """Input field to filter by username"""
        return self.page.locator('input[placeholder="Username"]').or_(self.page.locator('input[name="username"]'))

    @property
    def user_role_dropdown(self):
        """Dropdown to filter by user role"""
        return self.page.locator('div:has-text("User Role")').locator('i.oxd-select-text--arrow').or_(self.page.locator('div:has-text("-- Select --"):nth-child(2)'))

    @property
    def employee_name_filter(self):
        """Input field to filter by employee name"""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('input[name="employeeName"]'))

    @property
    def status_dropdown(self):
        """Dropdown to filter by status"""
        return self.page.locator('div:has-text("Status")').locator('i.oxd-select-text--arrow').or_(self.page.locator('div:has-text("-- Select --"):nth-child(3)'))

    @property
    def reset_button(self):
        """Button to reset the filter"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def search_button(self):
        """Button to apply the filter"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def first_username_in_table(self):
        """first username listed"""
        return self.page.locator('div.oxd-table-body div.oxd-table-card:nth-child(1) div:nth-child(2)').or_(self.page.locator('div.oxd-table-body div.oxd-table-card:nth-child(1) div:nth-child(2)'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.locator('h6.oxd-text--h6').first()).to_have_text('System Users')
        await expect(page).to_have_url(/admin/saveSystemUser)