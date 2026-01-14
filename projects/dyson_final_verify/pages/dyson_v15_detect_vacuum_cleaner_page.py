from playwright.async_api import Page, expect

class DysonV15DetectVacuumCleanerPage:
    """
    This page is a search results page for 'Dyson V15 Detect' on the Dyson India website. It displays search suggestions and promotional banners.
    URL Pattern: https://www.dyson.in/dyson-v15-detect-vacuum-cleaner
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input_clear_button(self):
        """Button to clear the search input field."""
        return self.page.xpath=//button[@aria-label='Clear search'].or_(self.page.css=button[aria-label='Clear search'])

    @property
    def search_button(self):
        """Button to open the search functionality."""
        return self.page.xpath=//button[@aria-label='Open search'].or_(self.page.css=button[aria-label='Open search'])

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
    def dyson_air_purifiers_link(self):
        """Link to the Dyson Air Purifiers product page."""
        return self.page.text=Dyson Air Purifiers.or_(self.page.css=a[href*='air-purifiers'])

    @property
    def dyson_deals_link(self):
        """Link to the Dyson Deals product page."""
        return self.page.text=Dyson Deals.or_(self.page.css=a[href*='deals'])

    @property
    def exclusive_reward_points_banner_close_button(self):
        """Button to close the exclusive reward points banner."""
        return self.page.xpath=//button[@aria-label='Close'].or_(self.page.css=button[aria-label='Close'])

    @property
    def chat_button(self):
        """Button to open the live chat."""
        return self.page.xpath=//button[@aria-label='Open Live Chat'].or_(self.page.css=button[aria-label='Open Live Chat'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson V15 Detect'
        await Page contains the text 'Dyson V15 Detect'
        await Page contains the text 'Most searched for'