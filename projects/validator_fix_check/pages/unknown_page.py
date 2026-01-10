from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page displays a list of available products with their names, descriptions, prices, and 'Add to cart' buttons.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Name(self):
        """The name of the product."""
        return self.page.[class*='inventory_item_name'].or_(self.page.div.inventory_item_label a div)

    @property
    def Product Description(self):
        """The description of the product."""
        return self.page.[class*='inventory_item_desc'].or_(self.page.div.inventory_item_label div.inventory_item_desc)

    @property
    def Product Price(self):
        """The price of the product."""
        return self.page.[class*='inventory_item_price'].or_(self.page.div.inventory_item_label div.inventory_item_price)

    @property
    def Add to cart button(self):
        """Button to add the product to the shopping cart."""
        return self.page.[class*='btn_inventory'].or_(self.page.button[id^='add-to-cart'])

    @property
    def Products Header(self):
        """The header text of the page."""
        return self.page.text=Products.or_(self.page.div.header_secondary_container span.title)

    @property
    def Filter Products(self):
        """Dropdown to filter products by name or price."""
        return self.page.[data-test='product_sort_container'].or_(self.page.span.select_container select.product_sort_container)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Page contains a header with the text 'Products'
        await Each product has a name, description, price, and 'Add to cart' button