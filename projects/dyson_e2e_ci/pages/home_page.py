from playwright.async_api import Page, expect

class HomePage:
    """
    This is the search overlay on the Dyson India homepage. It allows users to search for products and provides suggestions based on popular searches.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field for entering search queries."""
        return self.page.//input[@type='search'].or_(self.page.input[placeholder='dyson.in'])

    @property
    def search_button(self):
        """Button to submit the search query."""
        return self.page.css=svg[aria-label='Search'].or_(self.page.css=button[aria-label='Submit search'])

    @property
    def close_search_overlay(self):
        """Button to close the search overlay."""
        return self.page.css=button[aria-label='Close search'].or_(self.page.text=X)

    @property
    def dyson_airstrait_straightener(self):
        """Link to Dyson Airstrait straightener product page."""
        return self.page.text=Dyson Airstrait™ straightener.or_(self.page.css=a[href*='airstrait'])

    @property
    def _new_dyson_airwrap_i_d_(self):
        """Link to Dyson Airwrap i.d. product page."""
        return self.page.text=*NEW* Dyson Airwrap i.d.™.or_(self.page.css=a[href*='airwrap-multi-styler'])

    @property
    def dyson_v8_absolute_vacuum(self):
        """Link to Dyson V8 Absolute Vacuum product page."""
        return self.page.text=Dyson V8 Absolute Vacuum.or_(self.page.css=a[href*='dyson-v8-absolute'])

    @property
    def dyson_vacuum_cleaners(self):
        """Link to Dyson Vacuum Cleaners product page."""
        return self.page.text=Dyson Vacuum Cleaners.or_(self.page.css=a[href*='vacuum-cleaners'])

    @property
    def dyson_air_purifiers(self):
        """Link to Dyson Air Purifiers product page."""
        return self.page.text=Dyson Air Purifiers.or_(self.page.css=a[href*='air-purifiers'])

    @property
    def dyson_deals(self):
        """Link to Dyson Deals product page."""
        return self.page.text=Dyson Deals.or_(self.page.css=a[href*='deals'])

    @property
    def dyson_airwrap_accessories(self):
        """Link to Dyson Airwrap accessories product page."""
        return self.page.text=Dyson Airwrap™ accessories.or_(self.page.css=a[href*='airwrap-accessories'])

    @property
    def product_registration(self):
        """Link to Product Registration page."""
        return self.page.text=Product Registration.or_(self.page.css=a[href*='product-registration'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the page title contains 'Dyson India'
        await Verify that the search input field is present
        await Verify that the 'Most searched for' section is displayed
        await Verify that the Dyson logo is visible