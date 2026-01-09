from playwright.async_api import Page, expect

class SystemUsersPage:
    """
    System Users page to manage user accounts
    URL Pattern: /admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for username"""
        return self.page.get_by_label('Username').or_(self.page.locator('input[placeholder="Username"]'))

    @property
    def user_role_dropdown(self):
        """Dropdown to select user role"""
        return self.page.locator('div:has-text("User Role")').locator('i.oxd-icon.bi-caret-down-fill').or_(self.page.locator('div:has-text("User Role")').locator('div.oxd-select-text--after'))

    @property
    def employee_name_input(self):
        """Input field for employee name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]'))

    @property
    def status_dropdown(self):
        """Dropdown to select user status"""
        return self.page.locator('div:has-text("Status")').locator('i.oxd-icon.bi-caret-down-fill').or_(self.page.locator('div:has-text("Status")').locator('div.oxd-select-text--after'))

    @property
    def reset_button(self):
        """Button to reset the search form"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    @property
    def search_button(self):
        """Button to search for users"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def add_button(self):
        """Button to add a new user"""
        return self.page.get_by_role('button', name='Add').or_(self.page.locator('button:has-text("Add")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6:has-text("System Users")')).to_be_visible()