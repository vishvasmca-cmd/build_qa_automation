from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    The Saucedemo Inventory Page displays a list of available products with their descriptions, prices, and 'Add to cart' or 'Remove' buttons.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Name(self):
        """The name of the product."""
        return self.page.//div[@class='inventory_item_label']/a/div[@class='inventory_item_name'].or_(self.page..inventory_item_name)

    @property
    def Product Description(self):
        """The description of the product."""
        return self.page.//div[@class='inventory_item_label']/div[@class='inventory_item_desc'].or_(self.page..inventory_item_desc)

    @property
    def Product Price(self):
        """The price of the product."""
        return self.page.//div[@class='inventory_item_label']/div[@class='inventory_item_price'].or_(self.page..inventory_item_price)

    @property
    def Add to cart button(self):
        """Button to add the product to the shopping cart."""
        return self.page.//button[contains(@id, 'add-to-cart')].or_(self.page.button:contains('Add to cart'))

    @property
    def Remove button(self):
        """Button to remove the product from the shopping cart."""
        return self.page.//button[contains(@id, 'remove')].or_(self.page.button:contains('Remove'))

    @property
    def Products Header(self):
        """The 'Products' header text."""
        return self.page.//span[@class='title'].or_(self.page.span.title)

    @property
    def Filter Dropdown(self):
        """Dropdown to filter products."""
        return self.page.[data-test='product_sort_container'].or_(self.page..product_sort_container)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await The 'Products' header is displayed
        await At least one product is displayed with its name, description, and price
        await The 'Add to cart' or 'Remove' button is displayed for each product