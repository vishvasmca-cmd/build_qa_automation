from playwright.async_api import Page, expect

class WebInputsPageForAutomationTestingPracticePage:
    """
    This page is designed to practice and demonstrate web input functionalities for automation testing. It includes number and text input fields, along with buttons to display and clear the inputs.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Number Input(self):
        """Input field for entering numeric values."""
        return self.page.role=textbox[name="Input: Number"].or_(self.page.css=input[type='number'])

    @property
    def Text Input(self):
        """Input field for entering text values."""
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
        await Header text is 'Web inputs page for Automation Testing Practice'