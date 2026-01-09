from playwright.async_api import Page, expect

class RahulShettyAcademyPracticePagePage:
    """
    This page provides a variety of interactive elements for practicing UI automation, including radio buttons, dropdowns, checkboxes, input fields, tables, and window/tab handling.
    URL Pattern: https://rahulshettyacademy.com/AutomationPractice/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Radio Button 1(self):
        """First radio button option."""
        return self.page.id('radio-1').or_(self.page.css('input[value="radio1"]'))

    @property
    def Radio Button 2(self):
        """Second radio button option."""
        return self.page.id('radio-2').or_(self.page.css('input[value="radio2"]'))

    @property
    def Radio Button 3(self):
        """Third radio button option."""
        return self.page.id('radio-3').or_(self.page.css('input[value="radio3"]'))

    @property
    def Suggestion Class Input(self):
        """Input field for country suggestions."""
        return self.page.id('autocomplete').or_(self.page.css('#autocomplete'))

    @property
    def Dropdown(self):
        """Dropdown select element."""
        return self.page.id('dropdown-class-example').or_(self.page.css('#dropdown-class-example'))

    @property
    def Checkbox Option 1(self):
        """First checkbox option."""
        return self.page.id('checkBoxOption1').or_(self.page.css('#checkBoxOption1'))

    @property
    def Checkbox Option 2(self):
        """Second checkbox option."""
        return self.page.id('checkBoxOption2').or_(self.page.css('#checkBoxOption2'))

    @property
    def Checkbox Option 3(self):
        """Third checkbox option."""
        return self.page.id('checkBoxOption3').or_(self.page.css('#checkBoxOption3'))

    @property
    def Open Window Button(self):
        """Button to open a new window."""
        return self.page.id('openwindow').or_(self.page.css('#openwindow'))

    @property
    def Open Tab Button(self):
        """Button to open a new tab."""
        return self.page.id('opentab').or_(self.page.css('#opentab'))

    @property
    def Alert Input(self):
        """Input field for alert example."""
        return self.page.id('name').or_(self.page.css('#name'))

    @property
    def Alert Button(self):
        """Button to trigger an alert."""
        return self.page.id('alertbtn').or_(self.page.css('#alertbtn'))

    @property
    def Confirm Button(self):
        """Button to trigger a confirmation dialog."""
        return self.page.id('confirmbtn').or_(self.page.css('#confirmbtn'))

    @property
    def Hide Button(self):
        """Button to hide the associated textbox."""
        return self.page.id('hide-textbox').or_(self.page.css('#hide-textbox'))

    @property
    def Show Button(self):
        """Button to show the associated textbox."""
        return self.page.id('show-textbox').or_(self.page.css('#show-textbox'))

    @property
    def Hide/Show Example Textbox(self):
        """Textbox that can be hidden/shown."""
        return self.page.id('displayed-text').or_(self.page.css('#displayed-text'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Practice Page'
        await Page heading contains 'Practice Page'
        await Presence of 'Radio Button Example' section
        await Presence of 'Dropdown Example' section
        await Presence of 'Checkbox Example' section
        await Presence of 'Switch Window Example' section
        await Presence of 'Web Table Example' section