from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Dyson India. It showcases products, deals, and provides navigation to different product categories and support pages.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products_and_parts(self):
        """Search input field to find specific products or parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shop_now_button(self):
        """Button to navigate to the product page of the featured purifier."""
        return self.page.text=Shop now.or_(self.page.css=a[href='/en-IN/purifiers/compact'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners product category page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/en-IN/vacuum-cleaners'])

    @property
    def hair_care_link(self):
        """Link to the hair care product category page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/en-IN/hair-care'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier product category page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/en-IN/air-treatment'])

    @property
    def headphones_link(self):
        """Link to the headphones product category page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/en-IN/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting product category page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/en-IN/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/en-IN/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/en-IN/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title contains 'Dyson India'
        await Verify the Dyson logo is visible
        await Verify the 'Search products and parts' search box is present
        await Verify the presence of the featured product section (e.g., 'hushjet Purifier Compact')
        await Verify the presence of navigation links like 'Vacuum & wet cleaners', 'Hair care', etc.