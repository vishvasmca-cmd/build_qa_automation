from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    OrangeHRM Dashboard Page
    URL Pattern: /web/index.php/pim/viewEmployeeList
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
        """Card displaying quick action buttons"""
        return self.page.get_by_text('Quick Launch').or_(self.page.locator('div:has-text("Quick Launch")'))

    @property
    def Buzz Latest Posts Card(self):
        """Card displaying latest buzz posts"""
        return self.page.get_by_text('Buzz Latest Posts').or_(self.page.locator('div:has-text("Buzz Latest Posts")'))

    @property
    def Assign Leave Button(self):
        """Button to navigate to the Assign Leave page"""
        return self.page.get_by_text('Assign Leave').or_(self.page.locator('button:has-text("Assign Leave")'))

    @property
    def Leave List Button(self):
        """Button to navigate to the Leave List page"""
        return self.page.get_by_text('Leave List').or_(self.page.locator('button:has-text("Leave List")'))

    @property
    def Timesheets Button(self):
        """Button to navigate to the Timesheets page"""
        return self.page.get_by_text('Timesheets').or_(self.page.locator('button:has-text("Timesheets")'))

    @property
    def Apply Leave Button(self):
        """Button to navigate to the Apply Leave page"""
        return self.page.get_by_text('Apply Leave').or_(self.page.locator('button:has-text("Apply Leave")'))

    @property
    def My Leave Button(self):
        """Button to navigate to the My Leave page"""
        return self.page.get_by_text('My Leave').or_(self.page.locator('button:has-text("My Leave")'))

    @property
    def My Timesheet Button(self):
        """Button to navigate to the My Timesheet page"""
        return self.page.get_by_text('My Timesheet').or_(self.page.locator('button:has-text("My Timesheet")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.get_by_text('Dashboard')).to_be_visible()
        await expect(page.locator('div:has-text("Time at Work")')).to_be_visible()
        await expect(page.locator('div:has-text("My Actions")')).to_be_visible()
        await expect(page.locator('div:has-text("Quick Launch")')).to_be_visible()
        await expect(page.locator('div:has-text("Buzz Latest Posts")')).to_be_visible()