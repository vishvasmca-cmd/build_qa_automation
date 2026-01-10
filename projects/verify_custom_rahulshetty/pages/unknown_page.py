from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page is a practice page for UI automation, containing various interactive elements like radio buttons, dropdowns, checkboxes, input fields, buttons, and tables.
    URL Pattern: https://rahulshettyacademy.com/AutomationPractice/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Radio Button 1(self):
        """Radio button option 1"""
        return self.page.id('radio1').or_(self.page.xpath(//input[@value='radio1']))

    @property
    def Radio Button 2(self):
        """Radio button option 2"""
        return self.page.id('radio2').or_(self.page.xpath(//input[@value='radio2']))

    @property
    def Radio Button 3(self):
        """Radio button option 3"""
        return self.page.id('radio3').or_(self.page.xpath(//input[@value='radio3']))

    @property
    def Suggestion Class Input(self):
        """Input field for suggestion class example"""
        return self.page.id('autocomplete').or_(self.page.cssSelector(#autocomplete))

    @property
    def Dropdown(self):
        """Dropdown select element"""
        return self.page.id('dropdown-class-example').or_(self.page.cssSelector(#dropdown-class-example))

    @property
    def Checkbox Option 1(self):
        """Checkbox option 1"""
        return self.page.id('checkBoxOption1').or_(self.page.xpath(//input[@value='option1']))

    @property
    def Checkbox Option 2(self):
        """Checkbox option 2"""
        return self.page.id('checkBoxOption2').or_(self.page.xpath(//input[@value='option2']))

    @property
    def Checkbox Option 3(self):
        """Checkbox option 3"""
        return self.page.id('checkBoxOption3').or_(self.page.xpath(//input[@value='option3']))

    @property
    def Open Window Button(self):
        """Button to open a new window"""
        return self.page.id('openwindow').or_(self.page.cssSelector(#openwindow))

    @property
    def Open Tab Button(self):
        """Button to open a new tab"""
        return self.page.id('opentab').or_(self.page.cssSelector(#opentab))

    @property
    def Alert Input(self):
        """Input field for alert example"""
        return self.page.id('name').or_(self.page.cssSelector(#name))

    @property
    def Alert Button(self):
        """Button to trigger an alert"""
        return self.page.id('alertbtn').or_(self.page.cssSelector(#alertbtn))

    @property
    def Confirm Button(self):
        """Button to trigger a confirmation dialog"""
        return self.page.id('confirmbtn').or_(self.page.cssSelector(#confirmbtn))

    @property
    def Hide Button(self):
        """Button to hide the text box"""
        return self.page.id('hide-textbox').or_(self.page.cssSelector(#hide-textbox))

    @property
    def Show Button(self):
        """Button to show the text box"""
        return self.page.id('show-textbox').or_(self.page.cssSelector(#show-textbox))

    @property
    def Hide/Show Example Textbox(self):
        """Textbox that can be hidden or shown"""
        return self.page.id('displayed-text').or_(self.page.cssSelector(#displayed-text))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Practice Page'
        await Page heading contains 'Practice Page'
        await Radio button example section is present
        await Suggestion class example section is present
        await Dropdown example section is present
        await Checkbox example section is present
        await Switch window example section is present
        await Switch tab example section is present
        await Switch to alert example section is present
        await Web table example section is present
        await Element displayed example section is present