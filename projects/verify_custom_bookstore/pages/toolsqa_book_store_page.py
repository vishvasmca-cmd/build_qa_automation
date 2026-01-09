from playwright.async_api import Page, expect

class ToolsqaBookStorePage:
    """
    This page displays a list of books and allows users to search for books. It also provides links to other sections of the website.
    URL Pattern: https://demoqa.com/books
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Box(self):
        """Input field to search for books."""
        return self.page.//input[@id='searchBox'].or_(self.page.input#searchBox)

    @property
    def Search Button(self):
        """Button to initiate the book search."""
        return self.page.//button[@id='basic-addon2'].or_(self.page.button.input-group-text)

    @property
    def Login Button(self):
        """Button to navigate to the login page."""
        return self.page.//button[@id='login'].or_(self.page.button#login)

    @property
    def Book Title Link(self):
        """Link to the book details page."""
        return self.page.//a[contains(@href,'/book?book=')].or_(self.page.a[href*='/book?book='])

    @property
    def Book Store Application Menu(self):
        """Menu item to access the Book Store Application section."""
        return self.page.//div[@class='element-group'][6]//div[@class='header-wrapper'].or_(self.page.div.element-group:nth-child(6) div.header-wrapper)

    @property
    def Login Menu(self):
        """Menu item to navigate to the Login page."""
        return self.page.//li[@id='item-0']//span[@class='text' and text()='Login'].or_(self.page.li#item-0 span.text)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'DEMOQA'
        await Search box is present
        await Login button is present
        await At least one book title is displayed