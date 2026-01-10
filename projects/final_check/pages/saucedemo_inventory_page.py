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
        """The name of the product."""
        return self.page.[data-test*='title'].or_(self.page..inventory_item_name)

    @property
    def Product Description(self):
        """The description of the product."""
        return self.page..inventory_item_desc.or_(self.page..inventory_item_label > div:nth-child(2))

    @property
    def Product Price(self):
        """The price of the product."""
        return self.page..inventory_item_price.or_(self.page..inventory_item_label > div.inventory_item_price)

    @property
    def Add to Cart Button(self):
        """Button to add the product to the shopping cart."""
        return self.page.[data-test^='add-to-cart'].or_(self.page.button:contains('Add to cart'))

    @property
    def Product Image(self):
        """Image of the product."""
        return self.page..inventory_item_img img.or_(self.page..inventory_item_img a > img)

    @property
    def Products Header(self):
        """The 'Products' header text."""
        return self.page.Products.or_(self.page.div.header_secondary_container > span)

    @property
    def Filter Products(self):
        """Dropdown to filter products by name or price."""
        return self.page.[data-test='product_sort_container'].or_(self.page.span.select_container)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await The 'Products' header is displayed
        await At least one product is displayed with a name, description, price, and 'Add to cart' button