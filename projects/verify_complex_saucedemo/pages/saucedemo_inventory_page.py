from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    The inventory page displays a list of available products with their descriptions, prices, and 'Add to cart' or 'Remove' buttons.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_name(self):
        """The name of the product."""
        return self.page.//div[@class='inventory_item_label']/a/div[@class='inventory_item_name'].or_(self.page..inventory_item_name)

    @property
    def product_description(self):
        """The description of the product."""
        return self.page.//div[@class='inventory_item_label']/div[@class='inventory_item_desc'].or_(self.page..inventory_item_desc)

    @property
    def product_price(self):
        """The price of the product."""
        return self.page.//div[@class='inventory_item_label']/div[@class='inventory_item_price'].or_(self.page..inventory_item_price)

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.//button[contains(@id, 'add-to-cart')].or_(self.page.button[class='btn btn_primary btn_small btn_inventory'])

    @property
    def remove_button(self):
        """Button to remove the product from the shopping cart."""
        return self.page.//button[contains(@id, 'remove')].or_(self.page.button[class='btn btn_secondary btn_small btn_inventory'])

    @property
    def products_header(self):
        """The header text of the inventory page."""
        return self.page.//span[@class='title'].or_(self.page..title)

    @property
    def filter_dropdown(self):
        """Dropdown to filter products by name or price."""
        return self.page.[data-test='product_sort_container'].or_(self.page..product_sort_container)

    @property
    def shopping_cart_link(self):
        """Link to the shopping cart page."""
        return self.page.shopping_cart_container.or_(self.page.a.shopping_cart_link)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify the page title is 'Swag Labs'
        await Verify the 'Products' header is displayed
        await Verify that at least one product is displayed with its name, description, and price
        await Verify that 'Add to cart' or 'Remove' buttons are displayed for each product