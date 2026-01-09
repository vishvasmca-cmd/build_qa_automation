from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page is a placeholder or example domain page, indicating that the domain is reserved for documentation purposes.
    URL Pattern: https://example.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Main Heading(self):
        """The main heading of the page."""
        return self.page.role=heading[name="Example Domain"].or_(self.page.css=h1)

    @property
    def Domain Description(self):
        """The description of the example domain."""
        return self.page.text="This domain is for use in documentation examples without needing permission. Avoid use in operations.".or_(self.page.css=body > div > p)

    @property
    def Learn More Link(self):
        """Link to learn more about example domains."""
        return self.page.role=link[name="Learn more"].or_(self.page.text="Learn more")

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Example Domain'
        await Main heading 'Example Domain' is displayed
        await Description text is present
        await Learn More link is present