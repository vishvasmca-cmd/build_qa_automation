from playwright.async_api import Page, expect

class HomePage:
    """
    The homepage of Dyson India, featuring a prominent search bar and links to popular product categories.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """Input field for searching Dyson products."""
        return self.page.//input[@type='search'].or_(self.page.input[placeholder='dyson.in'])

    @property
    def search_button(self):
        """Button to submit the search query."""
        return self.page.//button[@type='submit'].or_(self.page.button[aria-label='Open search'])

    @property
    def dyson_airstrait_straightener_link(self):
        """Link to the Dyson Airstrait straightener product page."""
        return self.page.//a[contains(text(),'Dyson Airstrait™ straightener')].or_(self.page.a[href*='airstrait'])

    @property
    def _new_dyson_airwrap_i_d_link(self):
        """Link to the Dyson Airwrap i.d. product page."""
        return self.page.//a[contains(text(),'*NEW* Dyson Airwrap i.d.™')].or_(self.page.a[href*='airwrap-multi-styler'])

    @property
    def dyson_v8_absolute_vacuum_link(self):
        """Link to the Dyson V8 Absolute Vacuum product page."""
        return self.page.//a[contains(text(),'Dyson V8 Absolute Vacuum')].or_(self.page.a[href*='v8-absolute'])

    @property
    def dyson_vacuum_cleaners_link(self):
        """Link to the Dyson Vacuum Cleaners product page."""
        return self.page.//a[contains(text(),'Dyson Vacuum Cleaners')].or_(self.page.a[href*='vacuum-cleaners'])

    @property
    def dyson_air_purifiers_link(self):
        """Link to the Dyson Air Purifiers product page."""
        return self.page.//a[contains(text(),'Dyson Air Purifiers')].or_(self.page.a[href*='air-purifiers'])

    @property
    def dyson_deals_link(self):
        """Link to the Dyson Deals page."""
        return self.page.//a[contains(text(),'Dyson Deals')].or_(self.page.a[href*='deals'])

    @property
    def dyson_airwrap_accessories_link(self):
        """Link to the Dyson Airwrap accessories page."""
        return self.page.//a[contains(text(),'Dyson Airwrap™ accessories')].or_(self.page.a[href*='airwrap-accessories'])

    @property
    def discover_dyson_link(self):
        """Link to the Discover Dyson page."""
        return self.page.//a[contains(text(),'Discover Dyson')].or_(self.page.a[href*='discover-dyson'])

    @property
    def for_business_link(self):
        """Link to the For business page."""
        return self.page.//a[contains(text(),'For business')].or_(self.page.a[href*='for-business'])

    @property
    def store_finder_link(self):
        """Link to the Store finder page."""
        return self.page.//a[contains(text(),'Store finder')].or_(self.page.a[href*='store-finder'])

    @property
    def register_machine_link(self):
        """Link to the Register machine page."""
        return self.page.//a[contains(text(),'Register machine')].or_(self.page.a[href*='register-machine'])

    @property
    def contact_us_link(self):
        """Link to the Contact us page."""
        return self.page.//a[contains(text(),'Contact us')].or_(self.page.a[href*='contact-us'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Dyson India'
        await Search input field is present
        await The 'Most searched for' section is displayed
        await Dyson logo is visible