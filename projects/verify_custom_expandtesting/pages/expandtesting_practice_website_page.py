from playwright.async_api import Page, expect

class ExpandtestingPracticeWebsitePage:
    """
    This page serves as a practice website for automation testing, providing various elements and scenarios for testing different automation tools and techniques.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Input(self):
        """Input field to search for specific examples or topics on the website."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search an example...'])

    @property
    def Search Button(self):
        """Button to initiate the search based on the entered text in the search input field."""
        return self.page.text=Search.or_(self.page.css=button[class*='et_pb_button'])

    @property
    def Test Cases Button(self):
        """Button to navigate to the Test Cases section of the website."""
        return self.page.text=Test Cases.or_(self.page.css=a[href*='test-cases'])

    @property
    def API Testing Button(self):
        """Button to navigate to the API Testing section of the website."""
        return self.page.text=API Testing.or_(self.page.css=a[href*='api-testing'])

    @property
    def XPath / CSS Button(self):
        """Button to navigate to the XPath/CSS section of the website."""
        return self.page.text=Xpath / Css.or_(self.page.css=a[href*='xpath-css'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Expandtesting Practice Website'
        await Page contains the header 'Automation Testing Practice WebSite for QA and Developers'
        await The search input field is present and visible
        await The 'Test Cases' button is present and visible