from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    The inventory page displays a list of available products with their names, descriptions, prices, and 'Add to cart' buttons. It also includes a sorting dropdown to change the order of the products.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Sort Dropdown(self):
        """Dropdown to sort products by name or price."""
        return self.page.data-test='product_sort_container'.or_(self.page.css=select[data-test='product_sort_container'])

    @property
    def Product Sort Option: Name (A to Z)(self):
        """Option to sort products by name from A to Z."""
        return self.page.text='Name (A to Z)'.or_(self.page.css=option[value='az'])

    @property
    def Product Sort Option: Name (Z to A)(self):
        """Option to sort products by name from Z to A."""
        return self.page.text='Name (Z to A)'.or_(self.page.css=option[value='za'])

    @property
    def Product Sort Option: Price (low to high)(self):
        """Option to sort products by price from low to high."""
        return self.page.text='Price (low to high)'.or_(self.page.css=option[value='lohi'])

    @property
    def Product Sort Option: Price (high to low)(self):
        """Option to sort products by price from high to low."""
        return self.page.text='Price (high to low)'.or_(self.page.css=option[value='hilo'])

    @property
    def Sauce Labs Backpack Add to cart button(self):
        """Button to add the Sauce Labs Backpack to the cart."""
        return self.page.data-test='add-to-cart-sauce-labs-backpack'.or_(self.page.text='Add to cart')

    @property
    def Sauce Labs Bike Light Add to cart button(self):
        """Button to add the Sauce Labs Bike Light to the cart."""
        return self.page.data-test='add-to-cart-sauce-labs-bike-light'.or_(self.page.text='Add to cart')

    @property
    def Sauce Labs Bolt T-Shirt Add to cart button(self):
        """Button to add the Sauce Labs Bolt T-Shirt to the cart."""
        return self.page.data-test='add-to-cart-sauce-labs-bolt-t-shirt'.or_(self.page.text='Add to cart')

    @property
    def Sauce Labs Fleece Jacket Add to cart button(self):
        """Button to add the Sauce Labs Fleece Jacket to the cart."""
        return self.page.data-test='add-to-cart-sauce-labs-fleece-jacket'.or_(self.page.text='Add to cart')

    @property
    def Sauce Labs Onesie Add to cart button(self):
        """Button to add the Sauce Labs Onesie to the cart."""
        return self.page.data-test='add-to-cart-sauce-labs-onesie'.or_(self.page.text='Add to cart')

    @property
    def Test.allTheThings() T-Shirt (Red) Add to cart button(self):
        """Button to add the Test.allTheThings() T-Shirt (Red) to the cart."""
        return self.page.data-test='add-to-cart-test.allthethings()-t-shirt-(red)'.or_(self.page.text='Add to cart')

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Page contains the 'Products' header
        await Product list is displayed