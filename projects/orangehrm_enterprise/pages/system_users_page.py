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
    def username_input(self):
        """Input field for username"""
        return self.page.locator('input[placeholder="Username"]').or_(self.page.locator('input[name="username"]'))

    @property
    def user_role_dropdown(self):
        """Dropdown to select user role"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').or_(self.page.locator('div[class*="oxd-select-text--after"]'))

    @property
    def employee_name_input(self):
        """Input field for employee name"""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('input[name="employeeName"]'))

    @property
    def status_dropdown(self):
        """Dropdown to select user status"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').or_(self.page.locator('div[class*="oxd-select-text--after"]'))

    @property
    def search_button(self):
        """Button to search for system users"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def reset_button(self):
        """Button to reset the search form"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def delete_button(self):
        """Button to delete a system user"""
        return self.page.locator('button[class*="oxd-icon-button--delete"]').or_(self.page.locator('i.bi-trash'))

    @property
    def edit_button(self):
        """Button to edit a system user"""
        return self.page.locator('button[class*="oxd-icon-button--edit"]').or_(self.page.locator('i.bi-pencil-fill'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page.get_by_text('System Users')).to_be_visible()
        await expect(page.locator('//h6[text()="System Users"]')).to_be_visible()
        await expect(page.locator('//div[text()="(16) Records Found"]')).to_be_visible()