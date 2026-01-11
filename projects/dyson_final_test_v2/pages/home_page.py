from playwright.async_api import Page, expect

class HomePage:
    """
    The Dyson India homepage presents product categories, promotions, and a subscription popup.
    URL Pattern: https://www.dyson.in/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Email Address Input(self):
        """Input field for entering the email address to subscribe."""
        return self.page.//input[@type='email'].or_(self.page.input[placeholder='Email Address*'])

    @property
    def Claim Offer Button(self):
        """Button to submit the email address and claim the offer."""
        return self.page.//button[contains(text(),'Claim offer')].or_(self.page.button[type='submit'])

    @property
    def Close Subscription Popup(self):
        """Button to close the subscription popup."""
        return self.page.//div[@class='email-capture']/button[@class='email-capture__close'].or_(self.page.button.email-capture__close)

    @property
    def Search Products and Parts(self):
        """Search input field"""
        return self.page.//input[@id='search-input'].or_(self.page.input[placeholder='Search products and parts'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Dyson'
        await Subscription popup is displayed
        await The 'Claim offer' button is present
        await The 'Email Address' input field is present