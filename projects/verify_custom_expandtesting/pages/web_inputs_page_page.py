from playwright.async_api import Page, expect

class WebInputsPagePage:
    """
    This page is designed to demonstrate and practice handling various web input types. It allows users to interact with different input fields and provides a platform for testing automation scripts related to input handling.
    URL Pattern: https://practice.expandtesting.com/inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Page Title(self):
        """The main heading of the page."""
        return self.page.role=heading[name="Web inputs page for Automation Testing Practice"].or_(self.page.text="Web inputs page for Automation Testing Practice")

    @property
    def Number Input Field(self):
        """Input field for entering numbers."""
        return self.page.role=spinbutton[name="Input: Number"].or_(self.page.css=input[type='number'])

    @property
    def Display Inputs Button(self):
        """Button to display the entered inputs."""
        return self.page.role=button[name="Display Inputs"].or_(self.page.text="Display Inputs")

    @property
    def Clear Inputs Button(self):
        """Button to clear the entered inputs."""
        return self.page.role=button[name="Clear Inputs"].or_(self.page.text="Clear Inputs")

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Web inputs page for Automation Testing Practice'
        await URL contains '/inputs'
        await Number input field is present
        await Display Inputs button is present
        await Clear Inputs button is present