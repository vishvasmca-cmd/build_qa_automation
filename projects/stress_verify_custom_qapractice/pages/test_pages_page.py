from playwright.async_api import Page, expect

class TestPagesPage:
    """
    A collection of practice pages for software testing and automation.
    URL Pattern: https://testpages.herokuapp.com/tags/javascript/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def pages_link(self):
        """Link to the pages section."""
        return self.page.get_by_role('link', name='Pages').or_(self.page.locator('text=Pages'))

    @property
    def apps_link(self):
        """Link to the apps section."""
        return self.page.get_by_role('link', name='Apps').or_(self.page.locator('text=Apps'))

    @property
    def challenges_link(self):
        """Link to the challenges section."""
        return self.page.get_by_role('link', name='Challenges').or_(self.page.locator('text=Challenges'))

    @property
    def reference_link(self):
        """Link to the reference section."""
        return self.page.get_by_role('link', name='Reference').or_(self.page.locator('text=Reference'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Test Pages For Automation Testing')
        await expect(page.get_by_role('heading', name='Software Testing Practice Pages')).to_be_visible()