from playwright.async_api import Page, expect

class WebInputsPageForAutomationTestingPracticePage:
    """
    This page is designed to practice web input automation. It contains various input fields and buttons for testing purposes.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Number Input(self):
        """Input field for entering numbers."""
        return self.page.input[type='number'].or_(self.page.input[placeholder='Number'])

    @property
    def Display Inputs Button(self):
        """Button to display the entered inputs."""
        return self.page.text=Display Inputs.or_(self.page.//button[text()='Display Inputs'])

    @property
    def Clear Inputs Button(self):
        """Button to clear the input fields."""
        return self.page.text=Clear Inputs.or_(self.page.//button[text()='Clear Inputs'])

    @property
    def Web inputs page for Automation Testing Practice Header(self):
        """Main header of the page."""
        return self.page.text=Web inputs page for Automation Testing Practice.or_(self.page.h1)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Web inputs page for Automation Testing Practice'
        await The main header 'Web inputs page for Automation Testing Practice' is displayed
        await The 'Number' input field is present
        await The 'Display Inputs' button is present
        await The 'Clear Inputs' button is present