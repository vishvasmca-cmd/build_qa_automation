from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    The Dashboard page provides an overview of key information and quick actions for the user.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dashboard Header(self):
        """The main header of the Dashboard page."""
        return self.page.xpath=//h6[text()='Dashboard'].or_(self.page.css=h6.oxd-text--h6.oxd-main-menu-item--name)

    @property
    def Time at Work Card(self):
        """Card displaying the user's time at work information."""
        return self.page.xpath=//div[contains(text(),'Time at Work')].or_(self.page.css=.orangehrm-attendance-card)

    @property
    def My Actions Card(self):
        """Card displaying the user's pending actions."""
        return self.page.xpath=//div[contains(text(),'My Actions')].or_(self.page.css=.orangehrm-todo-list)

    @property
    def Quick Launch Card(self):
        """Card displaying quick launch options."""
        return self.page.xpath=//div[contains(text(),'Quick Launch')].or_(self.page.css=.orangehrm-quick-launch)

    @property
    def Buzz Latest Posts Card(self):
        """Card displaying the latest posts from Buzz."""
        return self.page.xpath=//div[contains(text(),'Buzz Latest Posts')].or_(self.page.css=.orangehrm-buzz-news)

    @property
    def Assign Leave Quick Launch(self):
        """Button to navigate to the Assign Leave page."""
        return self.page.xpath=//div[contains(text(),'Assign Leave')].or_(self.page.css=.orangehrm-quick-launch-card:nth-child(1) .orangehrm-quick-launch-text)

    @property
    def Leave List Quick Launch(self):
        """Button to navigate to the Leave List page."""
        return self.page.xpath=//div[contains(text(),'Leave List')].or_(self.page.css=.orangehrm-quick-launch-card:nth-child(2) .orangehrm-quick-launch-text)

    @property
    def Timesheets Quick Launch(self):
        """Button to navigate to the Timesheets page."""
        return self.page.xpath=//div[contains(text(),'Timesheets')].or_(self.page.css=.orangehrm-quick-launch-card:nth-child(3) .orangehrm-quick-launch-text)

    @property
    def Apply Leave Quick Launch(self):
        """Button to navigate to the Apply Leave page."""
        return self.page.xpath=//div[contains(text(),'Apply Leave')].or_(self.page.css=.orangehrm-quick-launch-card:nth-child(4) .orangehrm-quick-launch-text)

    @property
    def My Leave Quick Launch(self):
        """Button to navigate to the My Leave page."""
        return self.page.xpath=//div[contains(text(),'My Leave')].or_(self.page.css=.orangehrm-quick-launch-card:nth-child(5) .orangehrm-quick-launch-text)

    @property
    def My Timesheet Quick Launch(self):
        """Button to navigate to the My Timesheet page."""
        return self.page.xpath=//div[contains(text(),'My Timesheet')].or_(self.page.css=.orangehrm-quick-launch-card:nth-child(6) .orangehrm-quick-launch-text)

    @property
    def User Profile Dropdown(self):
        """Dropdown button to access user profile options."""
        return self.page.className=oxd-userdropdown-name.or_(self.page.css=.oxd-userdropdown-name)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title contains 'OrangeHRM'
        await Verify the 'Dashboard' header is displayed
        await Verify the 'Time at Work' card is displayed
        await Verify the 'My Actions' card is displayed
        await Verify the 'Quick Launch' card is displayed
        await Verify the 'Buzz Latest Posts' card is displayed