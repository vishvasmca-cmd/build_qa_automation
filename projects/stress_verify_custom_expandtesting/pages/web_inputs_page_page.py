from playwright.async_api import Page, expect

class WebInputsPagePage:
    """
    Page to practice web input automation
    URL Pattern: /inputs
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def number_input(self):
        """Input field for numbers"""
        return self.page.get_by_label('Input: Number').or_(self.page.locator('input[type="number"]'))

    @property
    def text_input(self):
        """Input field for text"""
        return self.page.get_by_label('Input: Text').or_(self.page.locator('input[type="text"]'))

    @property
    def display_inputs_button(self):
        """Button to display the inputs"""
        return self.page.get_by_role('button', name='Display Inputs').or_(self.page.locator('text=Display Inputs'))

    @property
    def clear_inputs_button(self):
        """Button to clear the inputs"""
        return self.page.get_by_role('button', name='Clear Inputs').or_(self.page.locator('text=Clear Inputs'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Inputs')
        await expect(page.locator('h1', has_text='Web inputs page for Automation Testing Practice')).to_be_visible()