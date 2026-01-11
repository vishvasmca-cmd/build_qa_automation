from playwright.async_api import Page, expect

class DysonHairCarePage:
    """
    This page is the Dyson Hair Care landing page, showcasing various hair care products and related information.
    URL Pattern: https://www.dyson.in/air-treatment
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def hair_care_link(self):
        """Link to the main Hair Care section."""
        return self.page.role=link[name="Hair care"].or_(self.page.text=Hair care)

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox[name="Search products and parts"].or_(self.page.css=input[placeholder="Search products and parts"])

    @property
    def hair_stylers_link(self):
        """Link to the Hair Stylers product category."""
        return self.page.role=link[name="Hair stylers"].or_(self.page.text=Hair stylers)

    @property
    def hair_dryers_link(self):
        """Link to the Hair Dryers product category."""
        return self.page.role=link[name="Hair dryers"].or_(self.page.text=Hair dryers)

    @property
    def hair_straighteners_link(self):
        """Link to the Hair Straighteners product category."""
        return self.page.role=link[name="Hair straighteners"].or_(self.page.text=Hair straighteners)

    @property
    def shop_all_hair_care(self):
        """Link to the all Hair Care product category."""
        return self.page.role=link[name="Shop all hair care"].or_(self.page.text=Shop all hair care)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson Hair Care'
        await The 'Hair care' link is visible
        await The 'Search products and parts' search box is visible