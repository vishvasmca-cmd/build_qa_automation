from playwright.async_api import Page, expect

class DysonV15DetectVacuumCleanerPage:
    """
    This page is a search results page for 'Dyson V15 Detect' on the Dyson India website. It displays the search results and related suggestions.
    URL Pattern: https://www.dyson.in/dyson-v15-detect-vacuum-cleaner
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field to enter search queries."""
        return self.page.role=searchbox.or_(self.page.css=input[type='search'])

    @property
    def search_button(self):
        """Button to submit the search query."""
        return self.page.role=button[name='Submit search'].or_(self.page.css=button[aria-label='Submit search'])

    @property
    def dyson_airstrait_straightener_link(self):
        """Link to the Dyson Airstrait straightener product page."""
        return self.page.text=Dyson Airstrait™ straightener.or_(self.page.css=a[href*='airstrait'])

    @property
    def _new_dyson_airwrap_i_d_link(self):
        """Link to the Dyson Airwrap i.d. product page."""
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
    def cookie_accept_button(self):
        """Button to accept the cookie policy."""
        return self.page.text=Learn more.or_(self.page.css=a[href*='cookie-policy'])

    @property
    def exclusive_offer_close_button(self):
        """Button to close the exclusive offer banner."""
        return self.page.role=button[name='Close'].or_(self.page.text=X)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson V15 Detect'
        await Header text 'Dyson V15 Detect' is visible
        await Search input field is present
        await 'Most searched for' section is visible