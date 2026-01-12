from playwright.async_api import Page, expect

class CartPage:
    """
    This page displays the details of a product after it has been added to the cart. It allows the user to view the cart or continue shopping.
    URL Pattern: https://automationexercise.com/view_cart
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def view_cart_link(self):
        """Link to navigate to the cart page."""
        return self.page.//a[contains(text(),'View Cart')].or_(self.page.a[href='/view_cart'])

    @property
    def continue_shopping_button(self):
        """Button to continue shopping and close the modal."""
        return self.page.//button[contains(text(),'Continue Shopping')].or_(self.page.button[class='btn btn-success close-modal btn-block'])

    @property
    def product_name(self):
        """Name of the product added to the cart."""
        return self.page.//p[contains(text(),'Blue Cotton Indie Mickey Dress')].or_(self.page.div[class='product-information'] > h2)

    @property
    def product_price(self):
        """Price of the product."""
        return self.page.//span[contains(text(),'Rs. 1530')].or_(self.page.div[class='product-information'] > span)

    @property
    def product_quantity(self):
        """Quantity of the product."""
        return self.page.//input[@id='quantity'].or_(self.page.input[name='quantity'])

    @property
    def add_to_cart_button(self):
        """Button to add the product to the cart."""
        return self.page.//button[contains(text(),'Add to cart')].or_(self.page.button[class='btn btn-default cart'])

    @property
    def your_name_input(self):
        """Input field for entering your name for review."""
        return self.page.//input[@id='name'].or_(self.page.input[name='name'])

    @property
    def email_address_input(self):
        """Input field for entering your email address for review."""
        return self.page.//input[@id='email'].or_(self.page.input[name='email'])

    @property
    def add_review_here_input(self):
        """Textarea for entering your review."""
        return self.page.//textarea[@id='review'].or_(self.page.textarea[name='review'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the 'Added!' modal is displayed.
        await Verify that the product name is displayed correctly.
        await Verify that the product price is displayed correctly.
        await Verify that the 'View Cart' link is present.
        await Verify that the 'Continue Shopping' button is present.