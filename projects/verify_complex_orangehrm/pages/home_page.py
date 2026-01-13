from playwright.async_api import Page, expect

class HomePage:
    """
    This is the Dashboard page of the OrangeHRM application. It provides a summary view of key information and quick actions for the logged-in user.
    URL Pattern: https://www.orangehrm.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dashboard_menu_item(self):
        """Link to the Dashboard page in the main navigation menu."""
        return self.page.//span[text()='Dashboard'].or_(self.page.li.oxd-main-menu-item--active > a > span)

    @property
    def time_at_work_widget(self):
        """Widget displaying the user's time at work information."""
        return self.page.//p[text()='Time at Work'].or_(self.page.div.oxd-grid-item:nth-child(1) > div > div.oxd-text.oxd-text--p)

    @property
    def my_actions_widget(self):
        """Widget displaying the user's pending actions."""
        return self.page.//p[text()='My Actions'].or_(self.page.div.oxd-grid-item:nth-child(2) > div > div.oxd-text.oxd-text--p)

    @property
    def quick_launch_widget(self):
        """Widget displaying quick launch options."""
        return self.page.//p[text()='Quick Launch'].or_(self.page.div.oxd-grid-item:nth-child(3) > div > div.oxd-text.oxd-text--p)

    @property
    def assign_leave_quick_launch(self):
        """Quick launch button to assign leave."""
        return self.page.//p[text()='Assign Leave'].or_(self.page.div.orangehrm-quick-launch-card:nth-child(1) > div > p)

    @property
    def leave_list_quick_launch(self):
        """Quick launch button to view leave list."""
        return self.page.//p[text()='Leave List'].or_(self.page.div.orangehrm-quick-launch-card:nth-child(2) > div > p)

    @property
    def timesheets_quick_launch(self):
        """Quick launch button to access timesheets."""
        return self.page.//p[text()='Timesheets'].or_(self.page.div.orangehrm-quick-launch-card:nth-child(3) > div > p)

    @property
    def apply_leave_quick_launch(self):
        """Quick launch button to apply for leave."""
        return self.page.//p[text()='Apply Leave'].or_(self.page.div.orangehrm-quick-launch-card:nth-child(4) > div > p)

    @property
    def my_leave_quick_launch(self):
        """Quick launch button to view my leave."""
        return self.page.//p[text()='My Leave'].or_(self.page.div.orangehrm-quick-launch-card:nth-child(5) > div > p)

    @property
    def my_timesheet_quick_launch(self):
        """Quick launch button to view my timesheet."""
        return self.page.//p[text()='My Timesheet'].or_(self.page.div.orangehrm-quick-launch-card:nth-child(6) > div > p)

    @property
    def buzz_latest_posts_widget(self):
        """Widget displaying the latest posts from Buzz."""
        return self.page.//p[text()='Buzz Latest Posts'].or_(self.page.div.oxd-grid-item:nth-child(4) > div > div.oxd-text.oxd-text--p)

    @property
    def user_profile_dropdown(self):
        """Dropdown button to access user profile options."""
        return self.page.//span[@class='oxd-userdropdown-tab'].or_(self.page.span.oxd-userdropdown-tab)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'OrangeHRM'
        await Dashboard menu item is highlighted/active
        await Time at Work widget is displayed
        await My Actions widget is displayed
        await Quick Launch widget is displayed
        await Buzz Latest Posts widget is displayed