from playwright.async_api import Page, expect

class OrangehrmPage:
    """
    This is the Dashboard page of the OrangeHRM application, providing a summary of key information and quick actions.
    URL Pattern: /dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dashboard_Header(self):
        """The main header of the Dashboard page."""
        return self.page.get_by_text('Dashboard').or_(self.page.locator('h6.oxd-text--h6'))

    @property
    def Time_at_Work_Card(self):
        """Card displaying the employee's time at work information."""
        return self.page.get_by_text('Time at Work').or_(self.page.locator('div.orangehrm-attendance-card'))

    @property
    def Quick_Launch_Card(self):
        """Card containing quick action buttons."""
        return self.page.get_by_text('Quick Launch').or_(self.page.locator('div.orangehrm-quick-launch'))

    @property
    def My_Actions_Card(self):
        """Card displaying pending actions for the user."""
        return self.page.get_by_text('My Actions').or_(self.page.locator('div.orangehrm-todo-list'))

    @property
    def Assign_Leave_Button(self):
        """Button to navigate to the Assign Leave page."""
        return self.page.get_by_text('Assign Leave').or_(self.page.locator('div.orangehrm-quick-launch-card:nth-child(1) > div > button'))

    @property
    def Leave_List_Button(self):
        """Button to navigate to the Leave List page."""
        return self.page.get_by_text('Leave List').or_(self.page.locator('div.orangehrm-quick-launch-card:nth-child(2) > div > button'))

    @property
    def Timesheets_Button(self):
        """Button to navigate to the Timesheets page."""
        return self.page.get_by_text('Timesheets').or_(self.page.locator('div.orangehrm-quick-launch-card:nth-child(3) > div > button'))

    @property
    def Apply_Leave_Button(self):
        """Button to navigate to the Apply Leave page."""
        return self.page.get_by_text('Apply Leave').or_(self.page.locator('div.orangehrm-quick-launch-card:nth-child(4) > div > button'))

    @property
    def My_Leave_Button(self):
        """Button to navigate to the My Leave page."""
        return self.page.get_by_text('My Leave').or_(self.page.locator('div.orangehrm-quick-launch-card:nth-child(5) > div > button'))

    @property
    def My_Timesheet_Button(self):
        """Button to navigate to the My Timesheet page."""
        return self.page.get_by_text('My Timesheet').or_(self.page.locator('div.orangehrm-quick-launch-card:nth-child(6) > div > button'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6.oxd-main-menu-item--name')).to_have_text('Dashboard')
        await expect(page.locator('div.orangehrm-attendance-card')).to_be_visible()
        await expect(page.locator('div.orangehrm-quick-launch')).to_be_visible()
        await expect(page.locator('div.orangehrm-todo-list')).to_be_visible()