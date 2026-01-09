from playwright.async_api import Page, expect

class UiTestAutomationPlaygroundPage:
    """
    This page demonstrates the 'Dynamic ID' challenge in UI test automation, where element IDs change on each page load, requiring robust locator strategies.
    URL Pattern: http://uitestingplayground.com/dynamicid
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dynamic ID Link(self):
        """Link to the Dynamic ID challenge page."""
        return self.page.text=Dynamic ID.or_(self.page.css=a[href='/dynamicid'])

    @property
    def Home Link(self):
        """Link to the home page."""
        return self.page.text=Home.or_(self.page.css=a[href='/'])

    @property
    def Resources Link(self):
        """Link to the resources page."""
        return self.page.text=Resources.or_(self.page.css=a[href='/resources'])

    @property
    def UI Test Automation Playground Header(self):
        """Main header of the page."""
        return self.page.text=UI Test Automation Playground.or_(self.page.css=h1)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'UI Test Automation Playground'
        await Main header text is 'UI Test Automation Playground'
        await The 'Dynamic ID' link is present on the page.