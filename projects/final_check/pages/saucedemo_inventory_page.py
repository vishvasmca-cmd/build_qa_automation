from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    The inventory page displays a list of available products with their names, descriptions, prices, and 'Add to cart' buttons.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Name(self):
        """The name of the product, which is also a link to the product details page."""
        return self.page.[class*='inventory_item_name'].or_(self.page.CSS:.inventory_item_label a div)

    @property
    def Product Description(self):
        """The description of the product."""
        return self.page.[class*='inventory_item_desc'].or_(self.page.CSS:.inventory_item_label div.inventory_item_desc)

    @property
    def Product Price(self):
        """The price of the product."""
        return self.page.[class*='inventory_item_price'].or_(self.page.CSS:.inventory_item_pricebar div.inventory_item_price)

    @property
    def Add to Cart Button(self):
        """Button to add the product to the shopping cart."""
        return self.page.[class*='btn_inventory'].or_(self.page.Text:Add to cart)

    @property
    def Products Header(self):
        """The header text indicating the page displays products."""
        return self.page.Text:Products.or_(self.page.CSS:.title)

    @property
    def Filter/Sort Dropdown(self):
        """Dropdown to filter or sort the products."""
        return self.page.[data-test='product_sort_container'].or_(self.page.CSS:.product_sort_container)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Page URL is '/inventory.html'
        await At least one product is displayed
        await The 'Products' header is visible