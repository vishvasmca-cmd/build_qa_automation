from playwright.async_api import Page, expect

class ExpandtestingPracticePage:
    """
    This page provides a practice website for automation testing, offering various elements and examples for testing different automation tools and techniques.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Input(self):
        """Input field to search for specific examples or elements on the page."""
        return self.page.role=textbox[name="Search an example..."].or_(self.page.css=input[placeholder="Search an example..."])

    @property
    def Search Button(self):
        """Button to initiate the search based on the input in the search field."""
        return self.page.role=button[name="Search"].or_(self.page.css=button[class*='btn-primary'])

    @property
    def Test Cases Button(self):
        """Button to navigate to the test cases section."""
        return self.page.role=button[name="Test Cases"].or_(self.page.text=Test Cases)

    @property
    def API Testing Button(self):
        """Button to navigate to the API testing section."""
        return self.page.role=button[name="API Testing"].or_(self.page.text=API Testing)

    @property
    def XPath / Css Button(self):
        """Button to navigate to the XPath/CSS section."""
        return self.page.role=button[name="Xpath / Css"].or_(self.page.text=Xpath / Css)

    @property
    def Buy us a coffee(self):
        """Link to support the platform."""
        return self.page.text=Buy us a coffee.or_(self.page.css=a[href*='buymeacoffee'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Expandtesting Practice'
        await Page contains the header 'Automation Testing Practice WebSite for QA and Developers'
        await Search input field is present
        await Search button is present