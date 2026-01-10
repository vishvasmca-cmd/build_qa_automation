from playwright.async_api import Page, expect

class WebInputsPagePage:
    """
    This page is designed to allow users to input data into various fields and interact with web elements, providing a practice environment for automation testing.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Number Input Field(self):
        """Input field for entering numeric data."""
        return self.page.role=textbox[name="Input: Number"].or_(self.page.css=input[type='number'])

    @property
    def Text Input Field(self):
        """Input field for entering text data."""
        return self.page.role=textbox[name="Input: Text"].or_(self.page.css=input[type='text'])

    @property
    def Display Inputs Button(self):
        """Button to display the entered inputs."""
        return self.page.role=button[name="Display Inputs"].or_(self.page.text=Display Inputs)

    @property
    def Clear Inputs Button(self):
        """Button to clear the entered inputs."""
        return self.page.role=button[name="Clear Inputs"].or_(self.page.text=Clear Inputs)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Inputs'
        await Page heading contains 'Web inputs page for Automation Testing Practice'
        await The 'Number Input Field' is present
        await The 'Text Input Field' is present
        await The 'Display Inputs Button' is present
        await The 'Clear Inputs Button' is present