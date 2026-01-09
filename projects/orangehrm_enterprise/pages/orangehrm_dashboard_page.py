from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    This is the Dashboard page of the OrangeHRM application. It provides a summary of key information and quick access to frequently used features.
    URL Pattern: /web/index.php/dashboard
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def time_at_work_section(self):
        """Section displaying the employee's time at work information."""
        return self.page.locator('div:has-text("Time at Work")').or_(self.page.locator('div:has-text("Punched In")'))

    @property
    def my_actions_section(self):
        """Section displaying the employee's pending actions."""
        return self.page.locator('div:has-text("My Actions")').or_(self.page.locator('div:has-text("(1) Pending Self Review")'))

    @property
    def quick_launch_section(self):
        """Section displaying quick launch icons for common tasks."""
        return self.page.locator('div:has-text("Quick Launch")').or_(self.page.locator('div:has-text("Assign Leave")'))

    @property
    def buzz_latest_posts_section(self):
        """Section displaying the latest posts from the Buzz platform."""
        return self.page.locator('div:has-text("Buzz Latest Posts")').or_(self.page.locator('div:has-text("Video unavailable")'))

    @property
    def assign_leave_quick_launch(self):
        """Quick launch button to assign leave."""
        return self.page.locator('div[class*="quickLaunge"] span:has-text("Assign Leave")').or_(self.page.locator('div[class*="quickLaunge"] a:has-text("Assign Leave")'))

    @property
    def leave_list_quick_launch(self):
        """Quick launch button to view leave list."""
        return self.page.locator('div[class*="quickLaunge"] span:has-text("Leave List")').or_(self.page.locator('div[class*="quickLaunge"] a:has-text("Leave List")'))

    @property
    def timesheets_quick_launch(self):
        """Quick launch button to access timesheets."""
        return self.page.locator('div[class*="quickLaunge"] span:has-text("Timesheets")').or_(self.page.locator('div[class*="quickLaunge"] a:has-text("Timesheets")'))

    @property
    def apply_leave_quick_launch(self):
        """Quick launch button to apply for leave."""
        return self.page.locator('div[class*="quickLaunge"] span:has-text("Apply Leave")').or_(self.page.locator('div[class*="quickLaunge"] a:has-text("Apply Leave")'))

    @property
    def my_leave_quick_launch(self):
        """Quick launch button to view my leave."""
        return self.page.locator('div[class*="quickLaunge"] span:has-text("My Leave")').or_(self.page.locator('div[class*="quickLaunge"] a:has-text("My Leave")'))

    @property
    def my_timesheet_quick_launch(self):
        """Quick launch button to access my timesheet."""
        return self.page.locator('div[class*="quickLaunge"] span:has-text("My Timesheet")').or_(self.page.locator('div[class*="quickLaunge"] a:has-text("My Timesheet")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6.oxd-main-menu-item--name:has-text("Dashboard")')).to_be_visible()
        await expect(page.locator('div:has-text("Time at Work")')).to_be_visible()
        await expect(page.locator('div:has-text("My Actions")')).to_be_visible()
        await expect(page.locator('div:has-text("Quick Launch")')).to_be_visible()
        await expect(page.locator('div:has-text("Buzz Latest Posts")')).to_be_visible()