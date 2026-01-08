from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    Dashboard page for OrangeHRM
    URL Pattern: /pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dashboard_header(self):
        """Main Dashboard header text"""
        return self.page.get_by_text('Dashboard').or_(self.page.locator('h6.oxd-text--h6.oxd-main-menu-item--name'))

    @property
    def time_at_work_card(self):
        """Time at Work card"""
        return self.page.get_by_text('Time at Work').or_(self.page.locator('div.orangehrm-attendance-card'))

    @property
    def quick_launch_card(self):
        """Quick Launch card"""
        return self.page.get_by_text('Quick Launch').or_(self.page.locator('div.orangehrm-dashboard-widget-body'))

    @property
    def my_actions_card(self):
        """My Actions card"""
        return self.page.get_by_text('My Actions').or_(self.page.locator('div.orangehrm-todo-list'))

    @property
    def buzz_latest_posts(self):
        """Buzz Latest Posts card"""
        return self.page.get_by_text('Buzz Latest Posts').or_(self.page.locator('div.orangehrm-buzz-widget'))

    @property
    def assign_leave_shortcut(self):
        """Assign Leave shortcut in Quick Launch card"""
        return self.page.get_by_text('Assign Leave').or_(self.page.locator('div:nth-child(1) > div > div.orangehrm-dashboard-widget-body > div > a > div > span'))

    @property
    def leave_list_shortcut(self):
        """Leave List shortcut in Quick Launch card"""
        return self.page.get_by_text('Leave List').or_(self.page.locator('div:nth-child(2) > div > div.orangehrm-dashboard-widget-body > div > a > div > span'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_text('Dashboard')).to_be_visible()
        await expect(page.locator('div.orangehrm-attendance-card')).to_be_visible()
        await expect(page.locator('div.orangehrm-dashboard-widget-body')).to_be_visible()