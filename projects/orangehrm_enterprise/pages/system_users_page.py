from playwright.async_api import Page, expect

class SystemUsersPage:
    """
    System Users page for managing user accounts
    URL Pattern: /admin/viewSystemUsers
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_button(self):
        """Button to add a new system user"""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    @property
    def username_input(self):
        """Input field for username"""
        return self.page.locator('input[placeholder="Username"]').or_(self.page.locator('//label[text()="Username"]/following-sibling::input'))

    @property
    def user_role_dropdown(self):
        """Dropdown to select user role"""
        return self.page.locator('div:has-text("-- Select --")').or_(self.page.locator('//label[text()="User Role"]/following-sibling::div'))

    @property
    def employee_name_input(self):
        """Input field for employee name"""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('//label[text()="Employee Name"]/following-sibling::input'))

    @property
    def status_dropdown(self):
        """Dropdown to select user status"""
        return self.page.locator('div:has-text("-- Select --"):nth-child(2)').or_(self.page.locator('//label[text()="Status"]/following-sibling::div'))

    @property
    def search_button(self):
        """Button to search for users"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def reset_button(self):
        """Button to reset the search form"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6', has_text='System Users')).to_be_visible()
        await expect(page.locator('div', has_text='(13) Records Found')).to_be_visible()