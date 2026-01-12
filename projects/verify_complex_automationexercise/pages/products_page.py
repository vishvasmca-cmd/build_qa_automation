from playwright.async_api import Page, expect

class ProductsPage:
    """
    The Products page displays a list of available products, allowing users to browse and select items for purchase. It includes product details, filtering options, and review sections.
    URL Pattern: https://automationexercise.com/products
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def products_link(self):
        """Link to navigate to the products page."""
        return self.page.role=link[name="Products"].or_(self.page.text=Products)

    @property
    def category_women(self):
        """Button to filter products by Women category."""
        return self.page.role=button[name="Women"].or_(self.page.text=Women)

    @property
    def category_men(self):
        """Button to filter products by Men category."""
        return self.page.role=button[name="Men"].or_(self.page.text=Men)

    @property
    def category_kids(self):
        """Button to filter products by Kids category."""
        return self.page.role=button[name="Kids"].or_(self.page.text=Kids)

    @property
    def brand_polo(self):
        """Link to filter products by Polo brand."""
        return self.page.text=Polo.or_(self.page.text=Polo (6))

    @property
    def brand_h_m(self):
        """Link to filter products by H&M brand."""
        return self.page.text=H&M.or_(self.page.text=H&M (5))

    @property
    def product_name(self):
        """Name of the product displayed."""
        return self.page.text="Blue Cotton Indie Mickey Dress".or_(self.page.css=h2)

    @property
    def product_price(self):
        """Price of the product."""
        return self.page.text="Rs. 1530".or_(self.page.css=.product-information span)

    @property
    def product_quantity(self):
        """Input field to specify the quantity of the product."""
        return self.page.css=input[name="quantity"].or_(self.page.css=input[type="number"])

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.text="Add to cart".or_(self.page.css=.cart)

    @property
    def your_name_input(self):
        """Input field for the user's name when writing a review."""
        return self.page.css=input[name="name"].or_(self.page.placeholder="Your Name")

    @property
    def email_address_input(self):
        """Input field for the user's email address when writing a review."""
        return self.page.css=input[name="email"].or_(self.page.placeholder="Email Address")

    @property
    def add_review_here_textarea(self):
        """Textarea for the user to write their review."""
        return self.page.id=review.or_(self.page.placeholder="Add Review Here!")

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the page title contains 'Automation Exercise - Products'
        await Verify that the URL is 'https://automationexercise.com/products'
        await Verify that the 'Category' section is displayed
        await Verify that the 'Brands' section is displayed
        await Verify that at least one product is displayed