from playwright.async_api import Page, expect

class WebInputsPageForAutomationTestingPracticePage:
    """
    Page for practicing web input automation.
    URL Pattern: /inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def input_number(self):
        """Input field for numbers."""
        return self.page.get_by_label('Input: Number').or_(self.page.locator('input[type="number"]'))

    @property
    def display_inputs_button(self):
        """Button to display the entered inputs."""
        return self.page.get_by_text('Display Inputs').or_(self.page.locator('input[value="Display Inputs"]'))

    @property
    def clear_inputs_button(self):
        """Button to clear the entered inputs."""
        return self.page.get_by_text('Clear Inputs').or_(self.page.locator('input[value="Clear Inputs"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Web inputs page for Automation Testing Practice')
        await expect(page.get_by_role('heading', name='Web inputs page for Automation Testing Practice')).to_be_visible()