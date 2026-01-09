from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    This is the Dashboard page of the OrangeHRM application. It provides a summary of key information and quick access to frequently used features.
    URL Pattern: /web/index.php/dashboard
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def time_at_work_card(self):
        """Card displaying the employee's time at work information."""
        return self.page.locator('div:has-text("Time at Work")').or_(self.page.locator('div:has-text("Punched In")'))

    @property
    def my_actions_card(self):
        """Card displaying the employee's pending actions."""
        return self.page.locator('div:has-text("My Actions")').or_(self.page.locator('div:has-text("Pending Self Review")'))

    @property
    def quick_launch_card(self):
        """Card displaying quick launch options."""
        return self.page.locator('div:has-text("Quick Launch")').or_(self.page.locator('div:has-text("Assign Leave")'))

    @property
    def buzz_latest_posts_card(self):
        """Card displaying the latest buzz posts."""
        return self.page.locator('div:has-text("Buzz Latest Posts")').or_(self.page.locator('div:has-text("Video unavailable")'))

    @property
    def assign_leave_button(self):
        """Button to navigate to the assign leave page."""
        return self.page.locator('button:has-text("Assign Leave")').or_(self.page.locator('button:has-text("Assign Leave")'))

    @property
    def leave_list_button(self):
        """Button to navigate to the leave list page."""
        return self.page.locator('button:has-text("Leave List")').or_(self.page.locator('button:has-text("Leave List")'))

    @property
    def timesheets_button(self):
        """Button to navigate to the timesheets page."""
        return self.page.locator('button:has-text("Timesheets")').or_(self.page.locator('button:has-text("Timesheets")'))

    @property
    def apply_leave_button(self):
        """Button to navigate to the apply leave page."""
        return self.page.locator('button:has-text("Apply Leave")').or_(self.page.locator('button:has-text("Apply Leave")'))

    @property
    def my_leave_button(self):
        """Button to navigate to the my leave page."""
        return self.page.locator('button:has-text("My Leave")').or_(self.page.locator('button:has-text("My Leave")'))

    @property
    def my_timesheet_button(self):
        """Button to navigate to the my timesheet page."""
        return self.page.locator('button:has-text("My Timesheet")').or_(self.page.locator('button:has-text("My Timesheet")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url(/web/index.php/dashboard)
        await expect(page.locator('h6.oxd-text.oxd-text--h6.oxd-main-menu-item--name:has-text("Dashboard")')).to_be_visible()
        await expect(page.locator('div:has-text("Time at Work")')).to_be_visible()
        await expect(page.locator('div:has-text("My Actions")')).to_be_visible()
        await expect(page.locator('div:has-text("Quick Launch")')).to_be_visible()
        await expect(page.locator('div:has-text("Buzz Latest Posts")')).to_be_visible()