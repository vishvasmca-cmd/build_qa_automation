from playwright.async_api import Page, expect

class CheckoutPage:
    """
    This page represents the checkout page of the Dyson India website, where users can review their basket and proceed to payment.
    URL Pattern: https://www.dyson.in/checkout/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def continue_shopping_link(self):
        """Link to navigate back to the product listing or homepage."""
        return self.page.text=Continue Shopping.or_(self.page.css=a[href='/'])

    @property
    def product_quantity_increment_button(self):
        """Button to increase the quantity of a product in the basket."""
        return self.page.text=+.or_(self.page.css=button[aria-label='quantity-increment'])

    @property
    def product_quantity_decrement_button(self):
        """Button to decrease the quantity of a product in the basket."""
        return self.page.text=-.or_(self.page.css=button[aria-label='quantity-decrement'])

    @property
    def continue_to_checkout_button(self):
        """Button to proceed to the next step of the checkout process."""
        return self.page.text=Continue to checkout →.or_(self.page.css=button.checkout-module--checkoutButton--2j34H)

    @property
    def promotional_code_accordion(self):
        """Accordion to enter a promotional code."""
        return self.page.text=Have you got a promotional code?.or_(self.page.css=button.checkout-module--accordionHeader--1_345)

    @property
    def remove_item_from_basket(self):
        """Button to remove an item from the basket."""
        return self.page.text=Delete.or_(self.page.css=button[aria-label='Remove item'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Checkout'
        await Header text 'Your basket' is visible
        await Order Total is displayed
        await Continue to checkout button is visible