from playwright.async_api import Page, expect

class CartPage:
    """
    This page displays the user's cart and allows them to place an order by filling out the 'Place Order' form.
    URL Pattern: https://www.demoblaze.com/cart.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def place_order_button(self):
        """Button to open the 'Place Order' form."""
        return self.page.//button[text()='Place Order'].or_(self.page.css=button.btn.btn-success)

    @property
    def place_order_modal(self):
        """The 'Place Order' dialog/modal."""
        return self.page.//div[@class='modal fade show'].or_(self.page.css=div.modal.fade.show)

    @property
    def place_order_modal_title(self):
        """Title of the 'Place Order' modal."""
        return self.page.//div[@id='orderModalLabel'].or_(self.page.css=#orderModalLabel)

    @property
    def name_input(self):
        """Input field for the user's name."""
        return self.page.//input[@id='name'].or_(self.page.css=#name)

    @property
    def country_input(self):
        """Input field for the user's country."""
        return self.page.//input[@id='country'].or_(self.page.css=#country)

    @property
    def city_input(self):
        """Input field for the user's city."""
        return self.page.//input[@id='city'].or_(self.page.css=#city)

    @property
    def credit_card_input(self):
        """Input field for the user's credit card number."""
        return self.page.//input[@id='card'].or_(self.page.css=#card)

    @property
    def month_input(self):
        """Input field for the credit card expiration month."""
        return self.page.//input[@id='month'].or_(self.page.css=#month)

    @property
    def year_input(self):
        """Input field for the credit card expiration year."""
        return self.page.//input[@id='year'].or_(self.page.css=#year)

    @property
    def purchase_button(self):
        """Button to submit the order."""
        return self.page.//button[text()='Purchase'].or_(self.page.css=button.btn.btn-primary)

    @property
    def close_button(self):
        """Button to close the 'Place Order' modal."""
        return self.page.//button[@aria-label='Close'].or_(self.page.css=button.close)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'STORE'
        await URL is 'https://www.demoblaze.com/cart.html'
        await 'Place Order' button is visible
        await Total amount is displayed