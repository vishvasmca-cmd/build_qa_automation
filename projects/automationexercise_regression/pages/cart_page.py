from playwright.sync_api import Page, expect
from .base_page import BasePage

class CartPage(BasePage):
    """
    Page Object for the Shopping Cart page.
    Handles verification of cart contents.
    """
    def __init__(self, page: Page):
        super().__init__(page)

    # --- Locators ---
    @property
    def cart_items(self):
        """Locator for all rows in the cart table."""
        return self.page.locator("#cart_info_table tbody tr")
    
    @property
    def checkout_button(self):
        """Locator for the 'Proceed To Checkout' button."""
        return self.page.get_by_text("Proceed To Checkout")

    # --- Verifications ---
    def verify_item_count(self, count: int):
        """Assert that the cart contains a specific number of items."""
        expect(self.cart_items).to_have_count(count)

    def verify_product_in_cart(self, product_name: str):
         """Assert that a product with the given name is visible in the cart."""
         expect(self.cart_items.filter(has_text=product_name)).to_be_visible()
