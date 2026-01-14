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
        return self.page.//input[@type='search'].or_(self.page.input[placeholder='dyson.in'])

    @property
    def search_button(self):
        """Button to initiate the search."""
        return self.page.//button[@aria-label='Search'].or_(self.page.css=button[class*='search'])

    @property
    def dyson_airstrait_straightener(self):
        """Link to Dyson Airstrait straightener product page."""
        return self.page.//a[text()='Dyson Airstrait™ straightener'].or_(self.page.text=Dyson Airstrait™ straightener)

    @property
    def _new_dyson_airwrap_i_d_(self):
        """Link to *NEW* Dyson Airwrap i.d. product page."""
        return self.page.//a[text()='*NEW* Dyson Airwrap i.d.™'].or_(self.page.text=*NEW* Dyson Airwrap i.d.™)

    @property
    def dyson_v8_absolute_vacuum(self):
        """Link to Dyson V8 Absolute Vacuum product page."""
        return self.page.//a[text()='Dyson V8 Absolute Vacuum'].or_(self.page.text=Dyson V8 Absolute Vacuum)

    @property
    def dyson_vacuum_cleaners(self):
        """Link to Dyson Vacuum Cleaners product page."""
        return self.page.//a[text()='Dyson Vacuum Cleaners'].or_(self.page.text=Dyson Vacuum Cleaners)

    @property
    def dyson_air_purifiers(self):
        """Link to Dyson Air Purifiers product page."""
        return self.page.//a[text()='Dyson Air Purifiers'].or_(self.page.text=Dyson Air Purifiers)

    @property
    def dyson_deals(self):
        """Link to Dyson Deals page."""
        return self.page.//a[text()='Dyson Deals'].or_(self.page.text=Dyson Deals)

    @property
    def discover_dyson(self):
        """Link to Discover Dyson page."""
        return self.page.//a[text()='Discover Dyson'].or_(self.page.text=Discover Dyson)

    @property
    def for_business(self):
        """Link to For business page."""
        return self.page.//a[text()='For business'].or_(self.page.text=For business)

    @property
    def store_finder(self):
        """Link to Store finder page."""
        return self.page.//a[text()='Store finder'].or_(self.page.text=Store finder)

    @property
    def register_machine(self):
        """Link to Register machine page."""
        return self.page.//a[text()='Register machine'].or_(self.page.text=Register machine)

    @property
    def contact_us(self):
        """Link to Contact us page."""
        return self.page.//a[text()='Contact us'].or_(self.page.text=Contact us)

    @property
    def close_promotion(self):
        """Button to close the promotion banner."""
        return self.page.//button[@aria-label='Close'].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title of the page should contain 'Dyson'
        await The Dyson logo is visible
        await The search input field is present
        await The 'Discover Dyson' link is visible
        await The 'For business' link is visible