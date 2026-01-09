from playwright.async_api import Page, expect

class LetcodeInputPage:
    """
    This page provides various input fields to practice different input-related scenarios and learn about sendKeys(), Keyboard TAB, getAttribute(), clear(), and isEnabled() methods.
    URL Pattern: https://letcode.in/edit
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Enter your full Name Input(self):
        """Input field to enter the full name."""
        return self.page.role=textbox[name="Enter your full Name"].or_(self.page.css=input[placeholder='Enter your full Name'])

    @property
    def Append a text and press keyboard tab Input(self):
        """Input field to append text and press tab."""
        return self.page.role=textbox[name="Append a text and press keyboard tab"].or_(self.page.css=input[placeholder='Append a text and press keyboard tab'])

    @property
    def What is inside the text box Input(self):
        """Input field to check what is inside the text box."""
        return self.page.role=textbox[name="What is inside the text box"].or_(self.page.css=input[placeholder='What is inside the text box'])

    @property
    def Clear the text Input(self):
        """Input field to clear the text."""
        return self.page.role=textbox[name="Clear the text"].or_(self.page.css=input[placeholder='Clear the text'])

    @property
    def Confirm edit field is disabled Input(self):
        """Input field that is disabled."""
        return self.page.role=textbox[name="Confirm edit field is disabled"].or_(self.page.css=input[placeholder='Confirm edit field is disabled'])

    @property
    def Confirm text is readonly Input(self):
        """Input field that is readonly."""
        return self.page.role=textbox[name="Confirm text is readonly"].or_(self.page.css=input[placeholder='Confirm text is readonly'])

    @property
    def Watch tutorial Button(self):
        """Button to watch the tutorial."""
        return self.page.text=Watch tutorial.or_(self.page.css=button:has-text('Watch tutorial'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'LetCode - Testing Hub'
        await Page heading is 'Input'