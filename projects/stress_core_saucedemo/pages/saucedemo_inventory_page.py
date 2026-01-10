from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    The inventory page displays a list of available products with their names, descriptions, prices, and 'Add to cart' buttons. It also includes a sorting dropdown to change the order of the products.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Products Header(self):
        """The header text displaying 'Products'."""
        return self.page.text=Products.or_(self.page.css=.title)

    @property
    def Product Name(self):
        """Name of the product."""
        return self.page.css=.inventory_item_name.or_(self.page.css=.inventory_item_description > a > div)

    @property
    def Product Description(self):
        """Description of the product."""
        return self.page.css=.inventory_item_desc.or_(self.page.css=.inventory_item_description > div)

    @property
    def Product Price(self):
        """Price of the product."""
        return self.page.css=.inventory_item_price.or_(self.page.css=.inventory_item_description > div.inventory_item_price)

    @property
    def Add to Cart Button(self):
        """Button to add the product to the cart."""
        return self.page.text=Add to cart.or_(self.page.css=.btn_inventory)

    @property
    def Sorting Dropdown(self):
        """Dropdown to sort the products."""
        return self.page.css=[data-test='product_sort_container'].or_(self.page.css=.product_sort_container)

    @property
    def Sorting Option(self):
        """Sorting option to sort the products."""
        return self.page.text=Name (A to Z).or_(self.page.css=option[value='az'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Header text 'Products' is displayed
        await At least one product is displayed