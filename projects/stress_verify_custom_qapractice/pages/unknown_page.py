from playwright.async_api import Page, expect

class UnknownPage:
    """
    Page demonstrating JavaScript alerts, confirms, and prompts.
    URL Pattern: /pages/basics/alerts-javascript/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def show_alert_box_button(self):
        """Button to trigger a JavaScript alert box."""
        return self.page.get_by_role('button', name='Show alert box').or_(self.page.locator('input[value="Show alert box"]'))

    @property
    def show_confirm_box_button(self):
        """Button to trigger a JavaScript confirm box."""
        return self.page.get_by_role('button', name='Show confirm box').or_(self.page.locator('input[value="Show confirm box"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Alerts - JavaScript')
        await expect(page.get_by_role('heading', name='Alerts - JavaScript')).to_be_visible()