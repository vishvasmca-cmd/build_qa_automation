from playwright.async_api import Page, expect

class HomePage:
    """
    This is the search overlay on the Dyson India homepage. The primary purpose is to allow users to search for products and information on the Dyson website.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field for entering search queries."""
        return self.page.//input[@type='search'].or_(self.page.input[placeholder=''])

    @property
    def search_button(self):
        """Button to submit the search query."""
        return self.page.//button[@type='submit'].or_(self.page.button[aria-label='Submit search'])

    @property
    def close_search_overlay(self):
        """Button to close the search overlay."""
        return self.page.button[aria-label='Close search'].or_(self.page.button[class*='Close'])

    @property
    def dyson_airstrait_straightener(self):
        """Link to Dyson Airstrait straightener product page."""
        return self.page.//a[text()='Dyson Airstrait™ straightener'].or_(self.page.a[href*='airstrait'])

    @property
    def _new_dyson_airwrap_i_d_(self):
        """Link to Dyson Airwrap i.d. product page."""
        return self.page.//a[text()='*NEW* Dyson Airwrap i.d.™'].or_(self.page.a[href*='airwrap-multi-styler'])

    @property
    def dyson_v8_absolute_vacuum(self):
        """Link to Dyson V8 Absolute Vacuum product page."""
        return self.page.//a[text()='Dyson V8 Absolute Vacuum'].or_(self.page.a[href*='v8-absolute'])

    @property
    def dyson_vacuum_cleaners(self):
        """Link to Dyson Vacuum Cleaners product page."""
        return self.page.//a[text()='Dyson Vacuum Cleaners'].or_(self.page.a[href*='vacuum-cleaners'])

    @property
    def dyson_air_purifiers(self):
        """Link to Dyson Air Purifiers product page."""
        return self.page.//a[text()='Dyson Air Purifiers'].or_(self.page.a[href*='air-purifiers'])

    @property
    def dyson_deals(self):
        """Link to Dyson Deals product page."""
        return self.page.//a[text()='Dyson Deals'].or_(self.page.a[href*='deals'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Search input field is present
        await The text 'Most searched for' is visible
        await The Dyson logo is visible