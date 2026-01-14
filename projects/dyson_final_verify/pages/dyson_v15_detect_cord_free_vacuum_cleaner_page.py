from playwright.async_api import Page, expect

class DysonV15DetectCordFreeVacuumCleanerPage:
    """
    This page is a search results page for 'Dyson V15 Detect' on the Dyson India website. It displays search suggestions and related product categories.
    URL Pattern: https://www.dyson.in/dyson-v15-detect-vacuum-cleaner
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field for entering search queries."""
        return self.page.xpath=//input[@type='search'].or_(self.page.css=input[type='search'])

    @property
    def search_button(self):
        """Button to initiate the search."""
        return self.page.css=button[aria-label='Open search'].or_(self.page.xpath=//button[@aria-label='Open search'])

    @property
    def clear_search_button(self):
        """Button to clear the search input field."""
        return self.page.css=button[aria-label='Clear search'].or_(self.page.xpath=//button[@aria-label='Clear search'])

    @property
    def dyson_airstrait_straightener_link(self):
        """Link to the Dyson Airstrait straightener product page."""
        return self.page.text=Dyson Airstrait™ straightener.or_(self.page.xpath=//a[text()='Dyson Airstrait™ straightener'])

    @property
    def _new_dyson_airwrap_i_d_link(self):
        """Link to the Dyson Airwrap i.d. product page."""
        return self.page.text=*NEW* Dyson Airwrap i.d.™.or_(self.page.xpath=//a[text()='*NEW* Dyson Airwrap i.d.™'])

    @property
    def dyson_v8_absolute_vacuum_link(self):
        """Link to the Dyson V8 Absolute Vacuum product page."""
        return self.page.text=Dyson V8 Absolute Vacuum.or_(self.page.xpath=//a[text()='Dyson V8 Absolute Vacuum'])

    @property
    def dyson_vacuum_cleaners_link(self):
        """Link to the Dyson Vacuum Cleaners product page."""
        return self.page.text=Dyson Vacuum Cleaners.or_(self.page.xpath=//a[text()='Dyson Vacuum Cleaners'])

    @property
    def dyson_air_purifiers_link(self):
        """Link to the Dyson Air Purifiers product page."""
        return self.page.text=Dyson Air Purifiers.or_(self.page.xpath=//a[text()='Dyson Air Purifiers'])

    @property
    def dyson_deals_link(self):
        """Link to the Dyson Deals product page."""
        return self.page.text=Dyson Deals.or_(self.page.xpath=//a[text()='Dyson Deals'])

    @property
    def dyson_airwrap_accessories_link(self):
        """Link to the Dyson Airwrap accessories product page."""
        return self.page.text=Dyson Airwrap™ accessories.or_(self.page.xpath=//a[text()='Dyson Airwrap™ accessories'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson V15 Detect'
        await The header 'Dyson V15 Detect' is displayed
        await The 'Most searched for' section is displayed