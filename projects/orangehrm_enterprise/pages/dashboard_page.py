from playwright.async_api import Page, expect

class DashboardPage:
    """
    Dashboard page for OrangeHRM
    URL Pattern: /dashboard
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Time at Work Card(self):
        """Card displaying employee time information"""
        return self.page.get_by_text('Time at Work').or_(self.page.locator('div:has-text("Time at Work")'))

    @property
    def My Actions Card(self):
        """Card displaying pending actions for the employee"""
        return self.page.get_by_text('My Actions').or_(self.page.locator('div:has-text("My Actions")'))

    @property
    def Quick Launch Card(self):
        """Card displaying quick actions"""
        return self.page.get_by_text('Quick Launch').or_(self.page.locator('div:has-text("Quick Launch")'))

    @property
    def Buzz Latest Posts Card(self):
        """Card displaying latest buzz posts"""
        return self.page.get_by_text('Buzz Latest Posts').or_(self.page.locator('div:has-text("Buzz Latest Posts")'))

    @property
    def Assign Leave Quick Launch(self):
        """Link to assign leave"""
        return self.page.get_by_text('Assign Leave').or_(self.page.locator('//div[@class="orangehrm-quick-launch-card"]//p[text()="Assign Leave"]'))

    @property
    def Leave List Quick Launch(self):
        """Link to leave list"""
        return self.page.get_by_text('Leave List').or_(self.page.locator('//div[@class="orangehrm-quick-launch-card"]//p[text()="Leave List"]'))

    @property
    def Timesheets Quick Launch(self):
        """Link to timesheets"""
        return self.page.get_by_text('Timesheets').or_(self.page.locator('//div[@class="orangehrm-quick-launch-card"]//p[text()="Timesheets"]'))

    @property
    def Apply Leave Quick Launch(self):
        """Link to apply leave"""
        return self.page.get_by_text('Apply Leave').or_(self.page.locator('//div[@class="orangehrm-quick-launch-card"]//p[text()="Apply Leave"]'))

    @property
    def My Leave Quick Launch(self):
        """Link to my leave"""
        return self.page.get_by_text('My Leave').or_(self.page.locator('//div[@class="orangehrm-quick-launch-card"]//p[text()="My Leave"]'))

    @property
    def My Timesheet Quick Launch(self):
        """Link to my timesheet"""
        return self.page.get_by_text('My Timesheet').or_(self.page.locator('//div[@class="orangehrm-quick-launch-card"]//p[text()="My Timesheet"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('//h6[text()="Dashboard"]')).to_be_visible()
        await expect(page.locator('//div[@class="orangehrm-dashboard-widget-name"]')).to_be_visible()