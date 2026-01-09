from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    The Dashboard page provides a summary view of key information and actions for the logged-in user, including time at work, pending actions, quick launch options, and recent buzz posts.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dashboard Header(self):
        """The main header text of the Dashboard page."""
        return self.page.xpath=//h6[text()='Dashboard'].or_(self.page.css=div[class*='header-title'] > h6)

    @property
    def Time at Work Widget(self):
        """Widget displaying the user's time at work information."""
        return self.page.xpath=//div[contains(text(),'Time at Work')].or_(self.page.css=div.orangehrm-attendance-card)

    @property
    def My Actions Widget(self):
        """Widget displaying the user's pending actions."""
        return self.page.xpath=//div[contains(text(),'My Actions')].or_(self.page.css=div.orangehrm-todo-list)

    @property
    def Leave Requests to Approve Link(self):
        """Link to the Leave Requests to Approve page."""
        return self.page.xpath=//a[contains(text(),'Leave Requests to Approve')].or_(self.page.text=(5) Leave Requests to Approve)

    @property
    def Quick Launch Widget(self):
        """Widget displaying quick launch options."""
        return self.page.xpath=//div[contains(text(),'Quick Launch')].or_(self.page.css=div.orangehrm-quick-launch)

    @property
    def Assign Leave Quick Launch(self):
        """Quick launch button to assign leave."""
        return self.page.xpath=//div[contains(text(),'Assign Leave')].or_(self.page.text=Assign Leave)

    @property
    def Buzz Latest Posts Widget(self):
        """Widget displaying the latest buzz posts."""
        return self.page.xpath=//div[contains(text(),'Buzz Latest Posts')].or_(self.page.css=div.orangehrm-buzz-news)

    @property
    def User Profile Dropdown(self):
        """Dropdown button to access user profile options."""
        return self.page.css=.oxd-userdropdown-name.or_(self.page.text=Alex Thomas)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the page title contains 'OrangeHRM'
        await Verify that the 'Dashboard' header is displayed
        await Verify that the 'Time at Work' widget is displayed
        await Verify that the 'My Actions' widget is displayed
        await Verify that the 'Quick Launch' widget is displayed
        await Verify that the 'Buzz Latest Posts' widget is displayed