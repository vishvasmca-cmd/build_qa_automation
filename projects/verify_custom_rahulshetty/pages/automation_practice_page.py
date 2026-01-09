from playwright.async_api import Page, expect

class AutomationPracticePage:
    """
    This page is designed to provide a variety of interactive elements for practicing and testing automation scripts. It includes examples of radio buttons, suggestion classes, dropdowns, checkboxes, window/tab switching, alerts, and web tables.
    URL Pattern: https://rahulshettyacademy.com/AutomationPractice/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Radio Button 1(self):
        """The first radio button option."""
        return self.page.id('radio1').or_(self.page.css('input[value="radio1"]'))

    @property
    def Suggestion Class Input(self):
        """Input field for suggestion class example."""
        return self.page.id('autocomplete').or_(self.page.css('#autocomplete'))

    @property
    def Dropdown Select(self):
        """Dropdown element for selecting an option."""
        return self.page.id('dropdown-class-example').or_(self.page.css('#dropdown-class-example'))

    @property
    def Checkbox Option 1(self):
        """The first checkbox option."""
        return self.page.id('checkBoxOption1').or_(self.page.css('#checkBoxOption1'))

    @property
    def Open Window Button(self):
        """Button to open a new window."""
        return self.page.id('openwindow').or_(self.page.text='Open Window')

    @property
    def Open Tab Button(self):
        """Button to open a new tab."""
        return self.page.id('opentab').or_(self.page.text='Open Tab')

    @property
    def Alert Input(self):
        """Input field for the alert example."""
        return self.page.id('name').or_(self.page.css('#name'))

    @property
    def Alert Button(self):
        """Button to trigger an alert."""
        return self.page.id('alertbtn').or_(self.page.text='Alert')

    @property
    def Confirm Button(self):
        """Button to trigger a confirmation dialog."""
        return self.page.id('confirmbtn').or_(self.page.text='Confirm')

    @property
    def Hide Button(self):
        """Button to hide the displayed element."""
        return self.page.id('hide-textbox').or_(self.page.text='Hide')

    @property
    def Show Button(self):
        """Button to show the hidden element."""
        return self.page.id('show-textbox').or_(self.page.text='Show')

    @property
    def Hide/Show Example Textbox(self):
        """Textbox that can be hidden or shown."""
        return self.page.id('displayed-text').or_(self.page.css('#displayed-text'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Practice Page'
        await Page contains the header 'Practice Page'
        await The 'Open Window' button is present
        await The 'Open Tab' button is present
        await The 'Alert' button is present