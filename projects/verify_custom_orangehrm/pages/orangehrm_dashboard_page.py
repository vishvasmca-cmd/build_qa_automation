from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    The Dashboard page of OrangeHRM provides a summary view of key information and quick actions for the logged-in user.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dashboard Menu Item(self):
        """Link to navigate to the Dashboard page."""
        return self.page.role=menuitem[name='Dashboard'].or_(self.page.text=Dashboard)

    @property
    def Time at Work(self):
        """Section displaying the user's time at work information."""
        return self.page.text=Time at Work.or_(self.page.css=.oxd-grid-item:nth-child(1))

    @property
    def My Actions(self):
        """Section displaying the user's pending actions."""
        return self.page.text=My Actions.or_(self.page.css=.oxd-grid-item:nth-child(2))

    @property
    def Buzz Latest Posts(self):
        """Section displaying the latest posts from the Buzz module."""
        return self.page.text=Buzz Latest Posts.or_(self.page.css=.oxd-grid-item:nth-child(3))

    @property
    def Quick Launch(self):
        """Section displaying quick launch icons."""
        return self.page.text=Quick Launch.or_(self.page.css=.oxd-grid-item:nth-child(4))

    @property
    def Assign Leave Quick Launch(self):
        """Quick launch icon to assign leave."""
        return self.page.text=Assign Leave.or_(self.page.css=.orangehrm-quick-launch-card:nth-child(1))

    @property
    def Leave List Quick Launch(self):
        """Quick launch icon to view leave list."""
        return self.page.text=Leave List.or_(self.page.css=.orangehrm-quick-launch-card:nth-child(2))

    @property
    def Timesheets Quick Launch(self):
        """Quick launch icon to access timesheets."""
        return self.page.text=Timesheets.or_(self.page.css=.orangehrm-quick-launch-card:nth-child(3))

    @property
    def Apply Leave Quick Launch(self):
        """Quick launch icon to apply for leave."""
        return self.page.text=Apply Leave.or_(self.page.css=.orangehrm-quick-launch-card:nth-child(4))

    @property
    def My Leave Quick Launch(self):
        """Quick launch icon to view my leave."""
        return self.page.text=My Leave.or_(self.page.css=.orangehrm-quick-launch-card:nth-child(5))

    @property
    def My Timesheet Quick Launch(self):
        """Quick launch icon to view my timesheet."""
        return self.page.text=My Timesheet.or_(self.page.css=.orangehrm-quick-launch-card:nth-child(6))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'OrangeHRM'
        await Header text is 'Dashboard'
        await Presence of 'Time at Work' section
        await Presence of 'My Actions' section
        await Presence of 'Quick Launch' section
        await Presence of 'Buzz Latest Posts' section