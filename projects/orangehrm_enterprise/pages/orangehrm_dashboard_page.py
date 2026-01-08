from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    OrangeHRM Dashboard Page
    URL Pattern: /dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dashboard_header(self):
        """The main header of the Dashboard page."""
        return self.page.get_by_role('heading', name='Dashboard').or_(self.page.locator('div[class*="oxd-topbar-header"] > div > span'))

    @property
    def time_at_work_card(self):
        """The 'Time at Work' card displaying attendance information."""
        return self.page.locator('div[class*="orangehrm-attendance-card"]').or_(self.page.locator('div[class*="orangehrm-dashboard-widget-container"]:has-text("Time at Work")'))

    @property
    def my_actions_card(self):
        """The 'My Actions' card displaying pending tasks."""
        return self.page.locator('div[class*="orangehrm-todo-list"]').or_(self.page.locator('div[class*="orangehrm-dashboard-widget-container"]:has-text("My Actions")'))

    @property
    def quick_launch_card(self):
        """The 'Quick Launch' card displaying shortcuts to common tasks."""
        return self.page.locator('div[class*="orangehrm-quick-launch"]').or_(self.page.locator('div[class*="orangehrm-dashboard-widget-container"]:has-text("Quick Launch")'))

    @property
    def buzz_latest_posts_card(self):
        """The 'Buzz Latest Posts' card displaying recent activity."""
        return self.page.locator('div[class*="orangehrm-buzz-widget"]').or_(self.page.locator('div[class*="orangehrm-dashboard-widget-container"]:has-text("Buzz Latest Posts")'))

    @property
    def assign_leave_quick_launch(self):
        """Quick launch link to assign leave."""
        return self.page.get_by_role('link', name='Assign Leave').or_(self.page.locator('div[class*="orangehrm-quick-launch-item"]:has-text("Assign Leave")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_role('heading', name='Dashboard')).to_be_visible()
        await expect(page.locator('div[class*="orangehrm-attendance-card"]')).to_be_visible()