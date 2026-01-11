from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the Dyson Support page, where users can find help, spare parts, and guides for their Dyson products.
    URL Pattern: https://www.dyson.in/support
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search products and parts(self):
        """Search input field to find products and parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def Solve a problem(self):
        """Link to the troubleshooting tool."""
        return self.page.text=Solve a problem.or_(self.page.css=div:nth-child(1) > div > h3)

    @property
    def Find the right part(self):
        """Link to find spare parts."""
        return self.page.text=Find the right part.or_(self.page.css=div:nth-child(2) > div > h3)

    @property
    def Tips, user guides and software updates(self):
        """Link to user guides and software updates."""
        return self.page.text=Tips, user guides and software updates.or_(self.page.css=div:nth-child(3) > div > h3)

    @property
    def Start troubleshooting(self):
        """Link to start troubleshooting."""
        return self.page.text=Start troubleshooting.or_(self.page.css=div:nth-child(1) > div > a)

    @property
    def Find parts(self):
        """Link to find parts."""
        return self.page.text=Find parts.or_(self.page.css=div:nth-child(2) > div > a)

    @property
    def See all tips and guides(self):
        """Link to see all tips and guides."""
        return self.page.text=See all tips and guides.or_(self.page.css=div:nth-child(3) > div > a)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Support'
        await Header text is 'Dyson Support'
        await Page contains 'Solve a problem, find spare parts and read expert tips and guides.'