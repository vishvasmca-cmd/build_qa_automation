from playwright.async_api import Page, expect

class OrangehrmDashboardPage:
    """
    Dashboard page for OrangeHRM application. Displays key information and quick access links.
    URL Pattern: /dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def time_at_work_section(self):
        """Section displaying employee time and attendance information."""
        return self.page.get_by_text('Time at Work').or_(self.page.locator('div:has-text("Time at Work")'))

    @property
    def my_actions_section(self):
        """Section displaying pending tasks and actions for the user."""
        return self.page.get_by_text('My Actions').or_(self.page.locator('div:has-text("My Actions")'))

    @property
    def quick_launch_section(self):
        """Section providing quick access links to common tasks."""
        return self.page.get_by_text('Quick Launch').or_(self.page.locator('div:has-text("Quick Launch")'))

    @property
    def buzz_latest_posts_section(self):
        """Section displaying latest posts from the Buzz social network."""
        return self.page.get_by_text('Buzz Latest Posts').or_(self.page.locator('div:has-text("Buzz Latest Posts")'))

    @property
    def upgrade_button(self):
        """Button to upgrade the OrangeHRM subscription."""
        return self.page.get_by_text('Upgrade').or_(self.page.locator('button:has-text("Upgrade")'))

    @property
    def user_dropdown(self):
        """Dropdown menu for user profile and settings."""
        return self.page.get_by_text('Mike user').or_(self.page.locator('span:has-text("Mike user")'))

    @property
    def admin_menu_item(self):
        """Link to the Admin module."""
        return self.page.get_by_text('Admin').or_(self.page.locator('a:has-text("Admin")'))

    @property
    def pim_menu_item(self):
        """Link to the PIM module."""
        return self.page.get_by_text('PIM').or_(self.page.locator('a:has-text("PIM")'))

    @property
    def leave_menu_item(self):
        """Link to the Leave module."""
        return self.page.get_by_text('Leave').or_(self.page.locator('a:has-text("Leave")'))

    @property
    def time_menu_item(self):
        """Link to the Time module."""
        return self.page.get_by_text('Time').or_(self.page.locator('a:has-text("Time")'))

    @property
    def recruitment_menu_item(self):
        """Link to the Recruitment module."""
        return self.page.get_by_text('Recruitment').or_(self.page.locator('a:has-text("Recruitment")'))

    @property
    def my_info_menu_item(self):
        """Link to the My Info module."""
        return self.page.get_by_text('My Info').or_(self.page.locator('a:has-text("My Info")'))

    @property
    def performance_menu_item(self):
        """Link to the Performance module."""
        return self.page.get_by_text('Performance').or_(self.page.locator('a:has-text("Performance")'))

    @property
    def dashboard_menu_item(self):
        """Link to the Dashboard module."""
        return self.page.get_by_text('Dashboard').or_(self.page.locator('a:has-text("Dashboard")'))

    @property
    def directory_menu_item(self):
        """Link to the Directory module."""
        return self.page.get_by_text('Directory').or_(self.page.locator('a:has-text("Directory")'))

    @property
    def maintenance_menu_item(self):
        """Link to the Maintenance module."""
        return self.page.get_by_text('Maintenance').or_(self.page.locator('a:has-text("Maintenance")'))

    @property
    def claim_menu_item(self):
        """Link to the Claim module."""
        return self.page.get_by_text('Claim').or_(self.page.locator('a:has-text("Claim")'))

    @property
    def buzz_menu_item(self):
        """Link to the Buzz module."""
        return self.page.get_by_text('Buzz').or_(self.page.locator('a:has-text("Buzz")'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6.oxd-main-menu-item--name:has-text("Dashboard")')).to_be_visible()
        await expect(page.locator('div:has-text("Time at Work")')).to_be_visible()
        await expect(page.locator('div:has-text("My Actions")')).to_be_visible()
        await expect(page.locator('div:has-text("Quick Launch")')).to_be_visible()
        await expect(page.locator('div:has-text("Buzz Latest Posts")')).to_be_visible()