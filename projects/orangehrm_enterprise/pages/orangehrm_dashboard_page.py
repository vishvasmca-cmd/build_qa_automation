from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    OrangeHRM Dashboard Page
    URL Pattern: /web/index.php/pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dashboard_header(self):
        """Dashboard header text"""
        return self.page.get_by_text('Dashboard').or_(self.page.locator('div.oxd-topbar-header-breadcrumb h6'))

    @property
    def time_at_work_card(self):
        """Time at Work card"""
        return self.page.get_by_text('Time at Work').or_(self.page.locator('div.orangehrm-attendance-card'))

    @property
    def my_actions_card(self):
        """My Actions card"""
        return self.page.get_by_text('My Actions').or_(self.page.locator('div.orangehrm-todo-list'))

    @property
    def quick_launch_card(self):
        """Quick Launch card"""
        return self.page.get_by_text('Quick Launch').or_(self.page.locator('div.orangehrm-quick-launch'))

    @property
    def buzz_latest_posts_card(self):
        """Buzz Latest Posts card"""
        return self.page.get_by_text('Buzz Latest Posts').or_(self.page.locator('div.orangehrm-buzz-news'))

    @property
    def assign_leave_quick_launch(self):
        """Assign Leave button in Quick Launch"""
        return self.page.get_by_text('Assign Leave').or_(self.page.locator('div.orangehrm-quick-launch-item:nth-child(1) div.orangehrm-quick-launch-item div.orangehrm-quick-launch-item--text'))

    @property
    def leave_list_quick_launch(self):
        """Leave List button in Quick Launch"""
        return self.page.get_by_text('Leave List').or_(self.page.locator('div.orangehrm-quick-launch-item:nth-child(2) div.orangehrm-quick-launch-item div.orangehrm-quick-launch-item--text'))

    @property
    def timesheets_quick_launch(self):
        """Timesheets button in Quick Launch"""
        return self.page.get_by_text('Timesheets').or_(self.page.locator('div.orangehrm-quick-launch-item:nth-child(3) div.orangehrm-quick-launch-item div.orangehrm-quick-launch-item--text'))

    @property
    def apply_leave_quick_launch(self):
        """Apply Leave button in Quick Launch"""
        return self.page.get_by_text('Apply Leave').or_(self.page.locator('div.orangehrm-quick-launch-item:nth-child(4) div.orangehrm-quick-launch-item div.orangehrm-quick-launch-item--text'))

    @property
    def my_leave_quick_launch(self):
        """My Leave button in Quick Launch"""
        return self.page.get_by_text('My Leave').or_(self.page.locator('div.orangehrm-quick-launch-item:nth-child(5) div.orangehrm-quick-launch-item div.orangehrm-quick-launch-item--text'))

    @property
    def my_timesheet_quick_launch(self):
        """My Timesheet button in Quick Launch"""
        return self.page.get_by_text('My Timesheet').or_(self.page.locator('div.orangehrm-quick-launch-item:nth-child(6) div.orangehrm-quick-launch-item div.orangehrm-quick-launch-item--text'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_text('Dashboard')).to_be_visible()
        await expect(page.locator('div.orangehrm-dashboard-widget-shell')).to_have_count(5)