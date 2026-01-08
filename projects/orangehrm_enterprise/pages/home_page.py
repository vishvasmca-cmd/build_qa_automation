from playwright.async_api import Page, expect

class HomePage:
    """
    Dashboard page providing an overview of employee-related information and quick actions.
    URL Pattern: /dashboard
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def upgrade_button(self):
        """Button to upgrade the OrangeHRM account."""
        return self.page.get_by_role('button', name='Upgrade').or_(self.page.locator('//a[text()="Upgrade"]'))

    @property
    def user_profile_dropdown(self):
        """Dropdown to access user profile and settings."""
        return self.page.get_by_role('button', name='Lucas userBorges').or_(self.page.locator('//span[@class="oxd-userdropdown-tab"]'))

    @property
    def assign_leave_quick_launch(self):
        """Quick launch icon to assign leave to an employee."""
        return self.page.get_by_text('Assign Leave').or_(self.page.locator('//div[text()="Assign Leave"]'))

    @property
    def leave_list_quick_launch(self):
        """Quick launch icon to view the leave list."""
        return self.page.get_by_text('Leave List').or_(self.page.locator('//div[text()="Leave List"]'))

    @property
    def timesheets_quick_launch(self):
        """Quick launch icon to access timesheets."""
        return self.page.get_by_text('Timesheets').or_(self.page.locator('//div[text()="Timesheets"]'))

    @property
    def apply_leave_quick_launch(self):
        """Quick launch icon to apply for leave."""
        return self.page.get_by_text('Apply Leave').or_(self.page.locator('//div[text()="Apply Leave"]'))

    @property
    def my_leave_quick_launch(self):
        """Quick launch icon to view my leave."""
        return self.page.get_by_text('My Leave').or_(self.page.locator('//div[text()="My Leave"]'))

    @property
    def my_timesheet_quick_launch(self):
        """Quick launch icon to view my timesheet."""
        return self.page.get_by_text('My Timesheet').or_(self.page.locator('//div[text()="My Timesheet"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('//h6[text()="Dashboard"]')).to_be_visible()
        await expect(page.locator('//p[text()="Time at Work"]')).to_be_visible()
        await expect(page.locator('//p[text()="My Actions"]')).to_be_visible()
        await expect(page.locator('//p[text()="Quick Launch"]')).to_be_visible()
        await expect(page.locator('//p[text()="Buzz Latest Posts"]')).to_be_visible()