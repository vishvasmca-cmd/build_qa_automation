from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page is a placeholder page for the example.com domain, indicating it's reserved for documentation purposes.
    URL Pattern: https://example.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Main Heading(self):
        """The main heading of the page."""
        return self.page.role=heading[name="Example Domain"].or_(self.page.css=body > div > h1)

    @property
    def Learn More Link(self):
        """Link to learn more about the domain."""
        return self.page.role=link[name="Learn more"].or_(self.page.text=Learn more)

    @property
    def Domain Description(self):
        """Description of the domain usage."""
        return self.page.text="This domain is for use in documentation examples without needing permission. Avoid use in operations.".or_(self.page.css=body > div > p)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Example Domain'
        await Main heading 'Example Domain' is present
        await Description text is present
        await 'Learn more' link is present