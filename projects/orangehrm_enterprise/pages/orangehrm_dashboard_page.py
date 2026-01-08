from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    Dashboard page for OrangeHRM
    URL Pattern: /dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def time_at_work_card(self):
        """Card displaying the employee's time at work information"""
        return self.page.locator('div:has-text("Time at Work")').or_(self.page.locator('div[class*="orangehrm-attendance-card"]'))

    @property
    def my_actions_card(self):
        """Card displaying the employee's pending actions"""
        return self.page.locator('div:has-text("My Actions")').or_(self.page.locator('div[class*="orangehrm-todo-list"]'))

    @property
    def quick_launch_card(self):
        """Card displaying quick launch options"""
        return self.page.locator('div:has-text("Quick Launch")').or_(self.page.locator('div[class*="orangehrm-quick-launch"]'))

    @property
    def buzz_latest_posts_card(self):
        """Card displaying the latest buzz posts"""
        return self.page.locator('div:has-text("Buzz Latest Posts")').or_(self.page.locator('div[class*="orangehrm-buzz-news"]'))

    @property
    def assign_leave_quick_launch(self):
        """Quick launch option to assign leave"""
        return self.page.get_by_text('Assign Leave').or_(self.page.locator('div[class*="orangehrm-quick-launch"] a:has-text("Assign Leave")'))

    @property
    def leave_list_quick_launch(self):
        """Quick launch option to view leave list"""
        return self.page.get_by_text('Leave List').or_(self.page.locator('div[class*="orangehrm-quick-launch"] a:has-text("Leave List")'))

    @property
    def timesheets_quick_launch(self):
        """Quick launch option to view timesheets"""
        return self.page.get_by_text('Timesheets').or_(self.page.locator('div[class*="orangehrm-quick-launch"] a:has-text("Timesheets")'))

    @property
    def apply_leave_quick_launch(self):
        """Quick launch option to apply for leave"""
        return self.page.get_by_text('Apply Leave').or_(self.page.locator('div[class*="orangehrm-quick-launch"] a:has-text("Apply Leave")'))

    @property
    def my_leave_quick_launch(self):
        """Quick launch option to view my leave"""
        return self.page.get_by_text('My Leave').or_(self.page.locator('div[class*="orangehrm-quick-launch"] a:has-text("My Leave")'))

    @property
    def my_timesheet_quick_launch(self):
        """Quick launch option to view my timesheet"""
        return self.page.get_by_text('My Timesheet').or_(self.page.locator('div[class*="orangehrm-quick-launch"] a:has-text("My Timesheet")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url(/dashboard)
        await expect(page.locator('h6.oxd-text--h6.oxd-main-menu-item--name:has-text("Dashboard")')).to_be_visible()
        await expect(page.locator('div:has-text("Time at Work")')).to_be_visible()