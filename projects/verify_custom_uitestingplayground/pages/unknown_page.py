from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page demonstrates the challenge of using dynamic IDs in UI automation. It contains a button with a dynamically generated ID.
    URL Pattern: http://uitestingplayground.com/dynamicid
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dynamic ID Button(self):
        """Button with a dynamic ID. Clicking this button should trigger an action (though the action itself isn't specified on this page)."""
        return self.page.role=button[name='Button with Dynamic ID'].or_(self.page.css=a.btn.btn-primary)

    @property
    def Dynamic ID Header(self):
        """The main header of the page."""
        return self.page.text=Dynamic ID.or_(self.page.css=h3)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'UI Testing Playground'
        await Page contains the 'Dynamic ID' header
        await Page contains a button with the text 'Button with Dynamic ID'