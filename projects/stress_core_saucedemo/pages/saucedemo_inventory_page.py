from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    The inventory page displays a list of available products with their names, descriptions, prices, and 'Add to cart' buttons. It also includes a sorting dropdown to change the order of the products.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Name(self):
        """The name of the product."""
        return self.page.//div[@class='inventory_item_name'].or_(self.page..inventory_item_name)

    @property
    def Product Description(self):
        """The description of the product."""
        return self.page.//div[@class='inventory_item_desc'].or_(self.page..inventory_item_desc)

    @property
    def Product Price(self):
        """The price of the product."""
        return self.page.//div[@class='inventory_item_price'].or_(self.page..inventory_item_price)

    @property
    def Add to cart button(self):
        """Button to add the product to the shopping cart."""
        return self.page.//button[contains(@id, 'add-to-cart')].or_(self.page.button[class*='btn_inventory'])

    @property
    def Sorting Dropdown(self):
        """Dropdown to sort the products by name or price."""
        return self.page.[data-test='product_sort_container'].or_(self.page..product_sort_container)

    @property
    def Sorting Option: Name (A to Z)(self):
        """Option to sort products by name (A to Z)."""
        return self.page.//option[@value='az'].or_(self.page.option[value='az'])

    @property
    def Sorting Option: Name (Z to A)(self):
        """Option to sort products by name (Z to A)."""
        return self.page.//option[@value='za'].or_(self.page.option[value='za'])

    @property
    def Sorting Option: Price (low to high)(self):
        """Option to sort products by price (low to high)."""
        return self.page.//option[@value='lohi'].or_(self.page.option[value='lohi'])

    @property
    def Sorting Option: Price (high to low)(self):
        """Option to sort products by price (high to low)."""
        return self.page.//option[@value='hilo'].or_(self.page.option[value='hilo'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Page contains the header 'Products'
        await At least one product is displayed