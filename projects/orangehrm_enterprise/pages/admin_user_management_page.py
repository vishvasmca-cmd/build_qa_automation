from playwright.async_api import Page, expect

class AdminUserManagementPage:
    """
    Admin User Management Page
    URL Pattern: /admin/viewSystemUsers
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_button(self):
        """Button to add a new user"""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    @property
    def username_filter(self):
        """Input field to filter users by username"""
        return self.page.locator('input[placeholder="Username"]').or_(self.page.locator('//label[text()="Username"]/following-sibling::input'))

    @property
    def user_role_dropdown(self):
        """Dropdown to filter users by user role"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').or_(self.page.locator('//label[text()="User Role"]/following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def employee_name_filter(self):
        """Input field to filter users by employee name"""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('//label[text()="Employee Name"]/following-sibling::input'))

    @property
    def status_dropdown(self):
        """Dropdown to filter users by status"""
        return self.page.locator('div[class*="oxd-select-text--arrow"]').or_(self.page.locator('//label[text()="Status"]/following-sibling::div//div[@class="oxd-select-text-input"]'))

    @property
    def search_button(self):
        """Button to apply the filter criteria"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def reset_button(self):
        """Button to clear the filter criteria"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6').first()).to_have_text('System Users')
        await expect(page.locator('button:has-text("+ Add")')).to_be_visible()