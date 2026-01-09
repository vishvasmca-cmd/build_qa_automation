from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page demonstrates the challenge of using dynamic IDs in UI automation and provides a button with a dynamic ID for testing purposes.
    URL Pattern: http://uitestingplayground.com/dynamicid
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dynamic ID Button(self):
        """Button with a dynamically generated ID."""
        return self.page.role=button.or_(self.page.text=Button with Dynamic ID)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'UITAP'
        await Page heading is 'Dynamic ID'
        await Button with Dynamic ID is visible