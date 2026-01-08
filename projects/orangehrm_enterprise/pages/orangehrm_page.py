from playwright.async_api import Page, expect

class OrangehrmPage:
    """
    Admin - System Users page in OrangeHRM
    URL Pattern: /admin/viewSystemUsers
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_button(self):
        """Button to add a new system user."""
        return self.page.get_by_role('button', name='+ Add').or_(self.page.locator('button:has-text("+ Add")'))

    @property
    def username_filter(self):
        """Input field to filter users by username."""
        return self.page.locator('input[placeholder="Username"]').or_(self.page.locator('div.oxd-input-field-bottom-space input'))

    @property
    def user_role_dropdown(self):
        """Dropdown to filter users by user role."""
        return self.page.locator('div:nth-child(2) > div > div:nth-child(2) > div > div > div.oxd-select-text--after > i').or_(self.page.locator('div:has-text("User Role") div.oxd-select-text'))

    @property
    def employee_name_filter(self):
        """Input field to filter users by employee name."""
        return self.page.locator('input[placeholder="Type for hints..."]').or_(self.page.locator('div:has-text("Employee Name") input'))

    @property
    def status_dropdown(self):
        """Dropdown to filter users by status."""
        return self.page.locator('div:nth-child(4) > div > div:nth-child(2) > div > div > div.oxd-select-text--after > i').or_(self.page.locator('div:has-text("Status") div.oxd-select-text'))

    @property
    def search_button(self):
        """Button to search for users based on the applied filters."""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button:has-text("Search")'))

    @property
    def reset_button(self):
        """Button to reset the filter criteria."""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button:has-text("Reset")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6').first()).to_have_text('System Users')
        await expect(page.locator('button:has-text("+ Add")')).to_be_visible()