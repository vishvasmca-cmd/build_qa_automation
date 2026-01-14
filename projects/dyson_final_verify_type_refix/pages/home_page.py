from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. The primary purpose is to allow users to search for products and navigate to different sections of the website.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field for searching Dyson products."""
        return self.page.css=input[type='search'].or_(self.page.css=form[role='search'] input)

    @property
    def search_button(self):
        """Button to initiate the search."""
        return self.page.css=button[aria-label='Open search'].or_(self.page.css=button[class*='search'])

    @property
    def dyson_airstrait_straightener_link(self):
        """Link to the Dyson Airstrait straightener product page."""
        return self.page.text=Dyson Airstrait™ straightener.or_(self.page.css=a[href*='airstrait'])

    @property
    def _new_dyson_airwrap_i_d_link(self):
        """Link to the Dyson Airwrap product page."""
        return self.page.text=*NEW* Dyson Airwrap i.d.™.or_(self.page.css=a[href*='airwrap'])

    @property
    def dyson_v8_absolute_vacuum_link(self):
        """Link to the Dyson V8 Absolute Vacuum product page."""
        return self.page.text=Dyson V8 Absolute Vacuum.or_(self.page.css=a[href*='v8-absolute'])

    @property
    def dyson_vacuum_cleaners_link(self):
        """Link to the Dyson Vacuum Cleaners product page."""
        return self.page.text=Dyson Vacuum Cleaners.or_(self.page.css=a[href*='vacuum-cleaners'])

    @property
    def cookie_banner_close_button(self):
        """Button to close the cookie banner."""
        return self.page.css=button[aria-label='Close'].or_(self.page.text=X)

    @property
    def chat_button(self):
        """Button to open the chat window."""
        return self.page.css=button[aria-label='Open chat'].or_(self.page.css=button[class*='chat'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Search input field is present
        await Dyson logo is visible
        await The text 'Most searched for' is present