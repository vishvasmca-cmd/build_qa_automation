from playwright.async_api import Page, expect

class AlertsJavascriptPage:
    """
    Page demonstrating JavaScript alerts, confirms, and prompts.
    URL Pattern: https://testpages.herokuapp.com/pages/basics/alerts-javascript/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def show_alert_box_button(self):
        """Button to trigger a JavaScript alert."""
        return self.page.get_by_role('button', name='Show alert box').or_(self.page.locator('#alertexamples'))

    @property
    def show_confirm_box_button(self):
        """Button to trigger a JavaScript confirm."""
        return self.page.get_by_role('button', name='Show confirm box').or_(self.page.locator('#confirmexample'))

    @property
    def show_prompt_box_button(self):
        """Button to trigger a JavaScript prompt."""
        return self.page.get_by_role('button', name='Show prompt box').or_(self.page.locator('#promptexample'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Alerts - JavaScript')
        await expect(page.get_by_role('heading', name='Alerts - JavaScript')).to_be_visible()