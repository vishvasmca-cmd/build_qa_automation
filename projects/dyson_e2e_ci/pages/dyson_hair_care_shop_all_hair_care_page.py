from playwright.async_api import Page, expect

class DysonHairCareShopAllHairCarePage:
    """
    This page displays all hair care products available on the Dyson India website. It allows users to browse and select products for purchase.
    URL Pattern: https://www.dyson.in/hair-care/shop-all-hair-care
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_products(self):
        """Input field to search for specific products or parts."""
        return self.page.role=searchbox.or_(self.page.css=input[placeholder='Search products and parts'])

    @property
    def shopping_cart_icon(self):
        """Link to the shopping cart page."""
        return self.page.role=link[name='Bag icon'].or_(self.page.css=a[aria-label='Bag icon'])

    @property
    def email_address_input(self):
        """Input field for entering email address to subscribe."""
        return self.page.role=textbox[name='Email Address *'].or_(self.page.css=input[type='email'])

    @property
    def claim_offer_button(self):
        """Button to submit the email address and claim the offer."""
        return self.page.role=button[name='Claim offer'].or_(self.page.text=Claim offer)

    @property
    def close_subscription_popup(self):
        """Button to close the subscription popup."""
        return self.page.role=button[name='Close'].or_(self.page.css=button[aria-label='Close'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Hair Care' or 'Dyson'
        await Verify that the 'Featured deals' section is displayed
        await Verify that the search input field is present
        await Verify that the 'Subscribe to Dyson' popup is displayed