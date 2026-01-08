from playwright.async_api import Page, expect

class OrangehrmLoginPage:
    """
    Dashboard page for logged-in users
    URL Pattern: /dashboard
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def time_at_work_header(self):
        """Heading for the Time at Work section"""
        return self.page.get_by_text('Time at Work').or_(self.page.locator('div:has-text("Time at Work")'))

    @property
    def my_actions_header(self):
        """Heading for the My Actions section"""
        return self.page.get_by_text('My Actions').or_(self.page.locator('div:has-text("My Actions")'))

    @property
    def quick_launch_header(self):
        """Heading for the Quick Launch section"""
        return self.page.get_by_text('Quick Launch').or_(self.page.locator('div:has-text("Quick Launch")'))

    @property
    def buzz_latest_posts_header(self):
        """Heading for the Buzz Latest Posts section"""
        return self.page.get_by_text('Buzz Latest Posts').or_(self.page.locator('div:has-text("Buzz Latest Posts")'))

    @property
    def user_dropdown(self):
        """User Dropdown"""
        return self.page.get_by_text('manda user').or_(self.page.locator('span.oxd-userdropdown-tab'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6.oxd-topbar-header-breadcrumb-module').text_contents()).to_equal('Dashboard')