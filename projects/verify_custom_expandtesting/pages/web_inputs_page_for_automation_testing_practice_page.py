from playwright.async_api import Page, expect

class WebInputsPageForAutomationTestingPracticePage:
    """
    This page is designed to practice and demonstrate web input functionalities for automation testing.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Input Number Field(self):
        """Text field for entering numeric input."""
        return self.page.input[type='number'].or_(self.page.css=input[type='number'])

    @property
    def Input Text Field(self):
        """Text field for entering text input."""
        return self.page.input[type='text'].or_(self.page.css=input[type='text'])

    @property
    def Display Inputs Button(self):
        """Button to display the entered inputs."""
        return self.page.text=Display Inputs.or_(self.page.css=button:has-text('Display Inputs'))

    @property
    def Clear Inputs Button(self):
        """Button to clear the entered inputs."""
        return self.page.text=Clear Inputs.or_(self.page.css=button:has-text('Clear Inputs'))

    @property
    def Web automation tools Link(self):
        """Link to Web automation tools."""
        return self.page.text=Web automation tools.or_(self.page.css=a:has-text('Web automation tools'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Web inputs page for Automation Testing Practice'
        await Header text is 'Web inputs page for Automation Testing Practice'
        await Input Number field is present
        await Input Text field is present
        await Display Inputs button is present
        await Clear Inputs button is present