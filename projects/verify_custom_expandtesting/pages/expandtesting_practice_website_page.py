from playwright.async_api import Page, expect

class ExpandtestingPracticeWebsitePage:
    """
    This page is an Automation Testing Practice Website for QA and Developers, providing resources and examples for various automation tools and techniques.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Input(self):
        """Input field to search for examples or resources."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search an example...'])

    @property
    def Search Button(self):
        """Button to initiate the search."""
        return self.page.text=Search.or_(self.page.css=button[class*='btn-primary'])

    @property
    def Test Cases Button(self):
        """Button to navigate to Test Cases examples."""
        return self.page.text=Test Cases.or_(self.page.css=button[class*='btn-info'])

    @property
    def API Testing Button(self):
        """Button to navigate to API Testing examples."""
        return self.page.text=API Testing.or_(self.page.css=button[class*='btn-warning'])

    @property
    def XPath / CSS Button(self):
        """Button to navigate to XPath/CSS examples."""
        return self.page.text=Xpath / Css.or_(self.page.css=button[class*='btn-success'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'ExpandTesting Practice'
        await Header text contains 'Automation Testing Practice WebSite for QA and Developers'
        await Search input field is present
        await Search button is present