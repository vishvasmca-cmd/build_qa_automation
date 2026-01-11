from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the Dyson Support page, which provides resources for troubleshooting, finding spare parts, and accessing user guides.
    URL Pattern: https://www.dyson.in/support
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Products and Parts(self):
        """Search input field for products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Solve a problem(self):
        """Link to the troubleshooting tool."""
        return self.page.text=Start troubleshooting.or_(self.page.css=a[href*='solve-a-problem'])

    @property
    def Find the right part(self):
        """Link to find spare parts."""
        return self.page.text=Find parts.or_(self.page.css=a[href*='find-parts'])

    @property
    def Tips, user guides and software updates(self):
        """Link to user guides and software updates."""
        return self.page.text=See all tips and guides.or_(self.page.css=a[href*='tips-and-guides'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Support'
        await Header text 'Dyson Support' is visible
        await Text 'Solve a problem, find spare parts and read expert tips and guides.' is visible
        await Text 'How can we help?' is visible