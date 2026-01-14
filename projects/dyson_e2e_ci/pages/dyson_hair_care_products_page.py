from playwright.async_api import Page, expect

class DysonHairCareProductsPage:
    """
    This page displays Dyson's hair care product range, allowing users to browse and shop for hair dryers, stylers, and accessories.
    URL Pattern: https://www.dyson.in/hair-care/shop-all-hair-care
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products(self):
        """Search input field to find specific products."""
        return self.page.aria/Search products and parts.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def email_address_input(self):
        """Input field for entering email address to subscribe."""
        return self.page.aria/Email Address *.or_(self.page.css=input[type='email'])

    @property
    def claim_offer_button(self):
        """Button to submit the email address and claim the offer."""
        return self.page.text=Claim offer.or_(self.page.css=button[type='submit'])

    @property
    def close_subscription_modal(self):
        """Button to close the subscription popup."""
        return self.page.aria/Close.or_(self.page.css=button[aria-label='Close'])

    @property
    def deals_link(self):
        """Link to the deals page."""
        return self.page.text=Deals.or_(self.page.css=a[href='/deals'])

    @property
    def vacuum_wet_cleaners_link(self):
        """Link to the vacuum cleaners page."""
        return self.page.text=Vacuum & wet cleaners.or_(self.page.css=a[href='/vacuum-cleaners'])

    @property
    def hair_care_link(self):
        """Link to the hair care page."""
        return self.page.text=Hair care.or_(self.page.css=a[href='/hair-care'])

    @property
    def air_purifier_link(self):
        """Link to the air purifier page."""
        return self.page.text=Air purifier.or_(self.page.css=a[href='/air-purifiers'])

    @property
    def headphones_link(self):
        """Link to the headphones page."""
        return self.page.text=Headphones.or_(self.page.css=a[href='/headphones'])

    @property
    def lighting_link(self):
        """Link to the lighting page."""
        return self.page.text=Lighting.or_(self.page.css=a[href='/lighting'])

    @property
    def support_link(self):
        """Link to the support page."""
        return self.page.text=Support.or_(self.page.css=a[href='/support'])

    @property
    def best_sellers_link(self):
        """Link to the best sellers page."""
        return self.page.text=Best sellers.or_(self.page.css=a[href='/best-sellers'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Hair Care | Dyson'
        await Page contains the text 'Featured deals'
        await Page contains the text 'Subscribe to Dyson. Get ₹500 off.'