from playwright.async_api import Page, expect

class SauceDemoInventoryPage:
    """
    The inventory page displays a list of available products with their descriptions, prices, and 'Add to cart' buttons.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_name(self):
        """The name of the product, which is also a link to the product details page."""
        return self.page.[data-test*='title'].or_(self.page..inventory_item_name)

    @property
    def product_description(self):
        """The description of the product."""
        return self.page..inventory_item_desc.or_(self.page..inventory_item_label > div:nth-child(2))

    @property
    def product_price(self):
        """The price of the product."""
        return self.page..inventory_item_price.or_(self.page..inventory_item_label > div.inventory_item_price)

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.[data-test*='add-to-cart'].or_(self.page..btn_primary)

    @property
    def product_sort_dropdown(self):
        """Dropdown to sort the products by name or price."""
        return self.page.[data-test='product_sort_container'].or_(self.page..product_sort_container)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await At least one product is displayed on the page
        await The 'Add to cart' button is visible for each product