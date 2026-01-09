from playwright.async_api import Page, expect

class RahulShettyAcademyPracticePagePage:
    """
    This page is designed to provide a variety of interactive elements for practicing automation testing techniques.
    URL Pattern: https://rahulshettyacademy.com/AutomationPractice/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def radio_button_1(self):
        """First radio button option"""
        return self.page.get_by_role('radio', name='Radio1').or_(self.page.locator('input[value="radio1"]'))

    @property
    def suggestion_input(self):
        """Input field for suggestion class example"""
        return self.page.locator('#autocomplete').or_(self.page.get_by_placeholder('Type to Select Countries'))

    @property
    def dropdown(self):
        """Dropdown select element"""
        return self.page.locator('#dropdown-class-example').or_(self.page.locator('select#dropdown-class-example'))

    @property
    def checkbox_1(self):
        """First checkbox option"""
        return self.page.get_by_role('checkbox', name='Option1').or_(self.page.locator('#checkBoxOption1'))

    @property
    def open_window_button(self):
        """Button to open a new window"""
        return self.page.locator('#openwindow').or_(self.page.get_by_text('Open Window'))

    @property
    def open_tab_button(self):
        """Button to open a new tab"""
        return self.page.locator('#opentab').or_(self.page.get_by_text('Open Tab'))

    @property
    def name_input(self):
        """Input field for alert example"""
        return self.page.locator('#name').or_(self.page.get_by_placeholder('Enter Your Name'))

    @property
    def alert_button(self):
        """Button to trigger an alert"""
        return self.page.locator('#alertbtn').or_(self.page.get_by_text('Alert'))

    @property
    def confirm_button(self):
        """Button to trigger a confirmation dialog"""
        return self.page.locator('#confirmbtn').or_(self.page.get_by_text('Confirm'))

    @property
    def hide_button(self):
        """Button to hide the displayed element"""
        return self.page.locator('#hide-textbox').or_(self.page.get_by_text('Hide'))

    @property
    def show_button(self):
        """Button to show the hidden element"""
        return self.page.locator('#show-textbox').or_(self.page.get_by_text('Show'))

    @property
    def hide_show_input(self):
        """Input field for hide/show example"""
        return self.page.locator('#displayed-text').or_(self.page.get_by_placeholder('Hide/Show Example'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Practice Page')
        await expect(page.locator('h1').with_text('Practice Page')).to_be_visible()