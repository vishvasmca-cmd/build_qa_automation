from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page displays advertisement content at the bottom of the page.
    URL Pattern: https://demoqa.com/books?book=9781449325862
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Advertisement 1(self):
        """First advertisement link"""
        return self.page.//div[contains(text(),'The Old Method')].or_(self.page.css=div:nth-child(1) > a > img)

    @property
    def Advertisement 2(self):
        """Third advertisement link"""
        return self.page.//div[contains(text(),'8 Things That Make Any Man Crave')].or_(self.page.css=div:nth-child(3) > a > img)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the advertisement section is displayed
        await Verify that the advertisement links are clickable