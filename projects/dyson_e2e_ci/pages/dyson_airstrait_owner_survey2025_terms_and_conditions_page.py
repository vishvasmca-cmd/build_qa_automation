from playwright.async_api import Page, expect

class DysonAirstraitOwnerSurvey2025TermsAndConditionsPage:
    """
    This page displays the terms and conditions for the Dyson Airstrait owner survey 2025.
    URL Pattern: https://www.dyson.in/footer-secondary-links/terms-and-conditions
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def dyson_logo(self):
        """Dyson logo that navigates to the homepage."""
        return self.page.role=link[name='Homepage'].or_(self.page.css=a[aria-label='Homepage'] > svg)

    @property
    def search_products_and_parts(self):
        """Search input box to find products and parts."""
        return self.page.role=searchbox[name='Search products and parts'].or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def dyson_airstrait_owner_survey_2025_heading(self):
        """Main heading of the terms and conditions page."""
        return self.page.role=heading[name='Dyson Airstrait™ owner Survey 2025'].or_(self.page.text='Dyson Airstrait™ owner Survey 2025')

    @property
    def terms_and_conditions_subheading(self):
        """Subheading indicating the content is about terms and conditions."""
        return self.page.role=heading[name='Terms and conditions'].or_(self.page.text='Terms and conditions')

    @property
    def form_link(self):
        """Link to the survey form."""
        return self.page.role=link[name='form'].or_(self.page.text='form')

    @property
    def dyson_in_link(self):
        """Link to the Dyson India website."""
        return self.page.role=link[name='www.dyson.in'].or_(self.page.text='www.dyson.in')

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Terms and Conditions'
        await Main heading 'Dyson Airstrait™ owner Survey 2025' is displayed
        await Terms and conditions text is present on the page
        await The URL is 'https://www.dyson.in/footer-secondary-links/terms-and-conditions'