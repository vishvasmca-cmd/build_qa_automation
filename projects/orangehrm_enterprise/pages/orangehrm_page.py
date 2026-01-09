from playwright.async_api import Page, expect

class OrangehrmPage:
    """
    The main dashboard page of the OrangeHRM application, providing an overview of key information and quick access to various modules.
    URL Pattern: /dashboard/index
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def admin_menu_item(self):
        """Link to navigate to the Admin module."""
        return self.page.get_by_role('link', name='Admin').or_(self.page.locator('//span[text()="Admin"]'))

    @property
    def pim_menu_item(self):
        """Link to navigate to the PIM (Personnel Information Management) module."""
        return self.page.get_by_role('link', name='PIM').or_(self.page.locator('//span[text()="PIM"]'))

    @property
    def leave_menu_item(self):
        """Link to navigate to the Leave module."""
        return self.page.get_by_role('link', name='Leave').or_(self.page.locator('//span[text()="Leave"]'))

    @property
    def time_menu_item(self):
        """Link to navigate to the Time module."""
        return self.page.get_by_role('link', name='Time').or_(self.page.locator('//span[text()="Time"]'))

    @property
    def recruitment_menu_item(self):
        """Link to navigate to the Recruitment module."""
        return self.page.get_by_role('link', name='Recruitment').or_(self.page.locator('//span[text()="Recruitment"]'))

    @property
    def my_info_menu_item(self):
        """Link to navigate to the My Info module."""
        return self.page.get_by_role('link', name='My Info').or_(self.page.locator('//span[text()="My Info"]'))

    @property
    def performance_menu_item(self):
        """Link to navigate to the Performance module."""
        return self.page.get_by_role('link', name='Performance').or_(self.page.locator('//span[text()="Performance"]'))

    @property
    def dashboard_menu_item(self):
        """Link to navigate to the Dashboard module."""
        return self.page.get_by_role('link', name='Dashboard').or_(self.page.locator('//span[text()="Dashboard"]'))

    @property
    def directory_menu_item(self):
        """Link to navigate to the Directory module."""
        return self.page.get_by_role('link', name='Directory').or_(self.page.locator('//span[text()="Directory"]'))

    @property
    def maintenance_menu_item(self):
        """Link to navigate to the Maintenance module."""
        return self.page.get_by_role('link', name='Maintenance').or_(self.page.locator('//span[text()="Maintenance"]'))

    @property
    def claim_menu_item(self):
        """Link to navigate to the Claim module."""
        return self.page.get_by_role('link', name='Claim').or_(self.page.locator('//span[text()="Claim"]'))

    @property
    def buzz_menu_item(self):
        """Link to navigate to the Buzz module."""
        return self.page.get_by_role('link', name='Buzz').or_(self.page.locator('//span[text()="Buzz"]'))

    @property
    def upgrade_button(self):
        """Button to upgrade the OrangeHRM instance."""
        return self.page.get_by_role('button', name='Upgrade').or_(self.page.locator('text=Upgrade'))

    @property
    def user_profile_dropdown(self):
        """Dropdown button to access user profile options."""
        return self.page.get_by_role('button', name='John Doe').or_(self.page.locator('.oxd-userdropdown-name'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('//h6[text()="Dashboard"]')).to_be_visible()
        await expect(page.locator('//p[text()="Time at Work"]')).to_be_visible()
        await expect(page.locator('//p[text()="My Actions"]')).to_be_visible()