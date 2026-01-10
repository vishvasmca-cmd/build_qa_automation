from playwright.async_api import Page, expect

class AutomationPracticePage:
    """
    This page is designed to provide a variety of interactive elements for practicing automation testing techniques.
    URL Pattern: https://rahulshettyacademy.com/AutomationPractice/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Radio Button 1(self):
        """First radio button option."""
        return self.page.id('radio-btn-example').or_(self.page.input[value='radio1'])

    @property
    def Radio Button 2(self):
        """Second radio button option."""
        return self.page.id('radio-btn-example').or_(self.page.input[value='radio2'])

    @property
    def Radio Button 3(self):
        """Third radio button option."""
        return self.page.id('radio-btn-example').or_(self.page.input[value='radio3'])

    @property
    def Suggestion Class Input(self):
        """Input field for suggestion class example."""
        return self.page.id('autocomplete').or_(self.page.input[placeholder='Enter Country'])

    @property
    def Dropdown Example(self):
        """Dropdown list for selecting an option."""
        return self.page.id('dropdown-class-example').or_(self.page.select[name='dropdown-class-example'])

    @property
    def Checkbox Option 1(self):
        """First checkbox option."""
        return self.page.id('checkbox-example').or_(self.page.input[value='option1'])

    @property
    def Checkbox Option 2(self):
        """Second checkbox option."""
        return self.page.id('checkbox-example').or_(self.page.input[value='option2'])

    @property
    def Checkbox Option 3(self):
        """Third checkbox option."""
        return self.page.id('checkbox-example').or_(self.page.input[value='option3'])

    @property
    def Open Window Button(self):
        """Button to open a new window."""
        return self.page.id('openwindow').or_(self.page.button[id='openwindow'])

    @property
    def Open Tab Button(self):
        """Button to open a new tab."""
        return self.page.id('opentab').or_(self.page.a[href='#top'])

    @property
    def Alert Input(self):
        """Input field for entering name for alert example."""
        return self.page.id('name').or_(self.page.input[name='enter-name'])

    @property
    def Alert Button(self):
        """Button to trigger an alert."""
        return self.page.id('alertbtn').or_(self.page.input[value='Alert'])

    @property
    def Confirm Button(self):
        """Button to trigger a confirmation dialog."""
        return self.page.id('confirmbtn').or_(self.page.input[value='Confirm'])

    @property
    def Hide Button(self):
        """Button to hide the displayed element."""
        return self.page.id('hide-textbox').or_(self.page.input[value='Hide'])

    @property
    def Show Button(self):
        """Button to show the hidden element."""
        return self.page.id('show-textbox').or_(self.page.input[value='Show'])

    @property
    def Hide/Show Example Textbox(self):
        """Textbox that can be hidden or shown."""
        return self.page.id('displayed-text').or_(self.page.input[name='show-hide'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Practice Page'
        await Page heading is 'Practice Page'
        await Radio Button Example section is present
        await Suggestion Class Example section is present
        await Dropdown Example section is present
        await Checkbox Example section is present
        await Switch Window Example section is present
        await Switch Tab Example section is present
        await Switch To Alert Example section is present
        await Web Table Example section is present
        await Element Displayed Example section is present