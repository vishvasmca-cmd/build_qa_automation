from playwright.async_api import Page, expect

class ProductsPage:
    """
    The Products page displays available products, categories, brands, and allows users to view product details, add to cart, and write reviews.
    URL Pattern: https://automationexercise.com/products
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def products_link(self):
        """Link to navigate to the products page."""
        return self.page.role=link[name=" Products"].or_(self.page.text= Products)

    @property
    def category_women(self):
        """Category filter for Women's products."""
        return self.page.role=button[name="Women"].or_(self.page.text=WOMEN)

    @property
    def category_men(self):
        """Category filter for Men's products."""
        return self.page.role=button[name="Men"].or_(self.page.text=MEN)

    @property
    def category_kids(self):
        """Category filter for Kids' products."""
        return self.page.role=button[name="Kids"].or_(self.page.text=KIDS)

    @property
    def brand_polo(self):
        """Brand filter for Polo products."""
        return self.page.role=link[name="Polo"].or_(self.page.text=POLO)

    @property
    def brand_h_m(self):
        """Brand filter for H&M products."""
        return self.page.role=link[name="H&M"].or_(self.page.text=H&M)

    @property
    def product_name(self):
        """Name of the displayed product."""
        return self.page.role=heading[name="Blue Cotton Indie Mickey Dress"].or_(self.page.text=Blue Cotton Indie Mickey Dress)

    @property
    def product_price(self):
        """Price of the displayed product."""
        return self.page.text=Rs. 1530.or_(self.page.text=Rs. 1530)

    @property
    def quantity_input(self):
        """Input field to specify the quantity of the product."""
        return self.page.role=spinbutton.or_(self.page.css=input[name='quantity'])

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.role=button[name="Add to cart"].or_(self.page.text=Add to cart)

    @property
    def your_name_input(self):
        """Input field for the user's name when writing a review."""
        return self.page.role=textbox[name="Your Name"].or_(self.page.css=input[name='name'])

    @property
    def email_address_input(self):
        """Input field for the user's email address when writing a review."""
        return self.page.role=textbox[name="Email Address"].or_(self.page.css=input[name='email'])

    @property
    def add_review_here_textarea(self):
        """Textarea for the user to write their product review."""
        return self.page.role=textbox[name="Add Review Here!"].or_(self.page.css=textarea#review)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the page title contains 'Automation Exercise - Products'
        await Verify that the URL is 'https://automationexercise.com/products'
        await Verify that the 'CATEGORY' section is visible
        await Verify that at least one product is displayed