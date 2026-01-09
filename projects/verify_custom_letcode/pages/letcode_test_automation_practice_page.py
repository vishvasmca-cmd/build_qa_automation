from playwright.async_api import Page, expect

class LetcodeTestAutomationPracticePage:
    """
    This page serves as a practice ground for test automation, providing various UI elements and scenarios to interact with.
    URL Pattern: https://letcode.in/edit
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def POM Card(self):
        """Link to the Page Object Model practice page."""
        return self.page.text=Page Object Model.or_(self.page.css=div:nth-child(1) > div > div > a)

    @property
    def Input Card(self):
        """Link to the Input practice page."""
        return self.page.text=Edit.or_(self.page.css=div:nth-child(2) > div > div > a)

    @property
    def Button Card(self):
        """Link to the Button practice page."""
        return self.page.text=Click.or_(self.page.css=div:nth-child(3) > div > div > a)

    @property
    def Select Card(self):
        """Link to the Select practice page."""
        return self.page.text=Drop-Down.or_(self.page.css=div:nth-child(4) > div > div > a)

    @property
    def Alert Card(self):
        """Link to the Alert practice page."""
        return self.page.text=Dialog.or_(self.page.css=div:nth-child(5) > div > div > a)

    @property
    def Frame Card(self):
        """Link to the Frame practice page."""
        return self.page.text=Inner HTML.or_(self.page.css=div:nth-child(6) > div > div > a)

    @property
    def Radio Card(self):
        """Link to the Radio practice page."""
        return self.page.text=Toggle.or_(self.page.css=div:nth-child(7) > div > div > a)

    @property
    def Window Card(self):
        """Link to the Window practice page."""
        return self.page.text=Tabs.or_(self.page.css=div:nth-child(8) > div > div > a)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'LetCode - Testing Hub'
        await Header text is 'Ready to be a Pro Engineer?'