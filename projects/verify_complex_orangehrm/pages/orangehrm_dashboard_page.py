from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    The Dashboard page provides a summary view of key information and quick actions for the user.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dashboard_menu_item(self):
        """Link to the Dashboard page in the main menu."""
        return self.page.[data-v-957b4417=''][class*='oxd-main-menu-item active'].or_(self.page.text=Dashboard)

    @property
    def time_at_work_card(self):
        """Card displaying the user's time at work information."""
        return self.page.text=Time at Work.or_(self.page.div:has-text('Time at Work'))

    @property
    def my_actions_card(self):
        """Card displaying the user's pending actions."""
        return self.page.text=My Actions.or_(self.page.div:has-text('My Actions'))

    @property
    def quick_launch_card(self):
        """Card displaying quick action links."""
        return self.page.text=Quick Launch.or_(self.page.div:has-text('Quick Launch'))

    @property
    def assign_leave_quick_launch(self):
        """Quick launch link to assign leave."""
        return self.page.text=Assign Leave.or_(self.page.Assign Leave)

    @property
    def leave_list_quick_launch(self):
        """Quick launch link to view leave list."""
        return self.page.text=Leave List.or_(self.page.Leave List)

    @property
    def timesheets_quick_launch(self):
        """Quick launch link to view timesheets."""
        return self.page.text=Timesheets.or_(self.page.Timesheets)

    @property
    def apply_leave_quick_launch(self):
        """Quick launch link to apply for leave."""
        return self.page.text=Apply Leave.or_(self.page.Apply Leave)

    @property
    def my_leave_quick_launch(self):
        """Quick launch link to view my leave."""
        return self.page.text=My Leave.or_(self.page.My Leave)

    @property
    def my_timesheet_quick_launch(self):
        """Quick launch link to view my timesheet."""
        return self.page.text=My Timesheet.or_(self.page.My Timesheet)

    @property
    def buzz_latest_posts_card(self):
        """Card displaying the latest buzz posts."""
        return self.page.text=Buzz Latest Posts.or_(self.page.div:has-text('Buzz Latest Posts'))

    @property
    def user_profile_dropdown(self):
        """Dropdown button to access user profile options."""
        return self.page.text=Peter Thomson.or_(self.page.span.oxd-userdropdown-name)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'OrangeHRM'
        await Dashboard menu item is active
        await Presence of 'Time at Work' card
        await Presence of 'My Actions' card
        await Presence of 'Quick Launch' card
        await Presence of 'Buzz Latest Posts' card