from playwright.async_api import Page, expect

class HomePage:
    """
    This is the inventory page of the Swag Labs demo application, displaying a list of available products.
    URL Pattern: https://www.saucedemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Sort Dropdown(self):
        """Dropdown to sort the products by different criteria (e.g., name, price)."""
        return self.page.[data-test='product_sort_container'].or_(self.page.css=.product_sort_container)

    @property
    def Add to cart button for Sauce Labs Backpack(self):
        """Button to add the Sauce Labs Backpack to the shopping cart."""
        return self.page.[data-test='add-to-cart-sauce-labs-backpack'].or_(self.page.text='Add to cart')

    @property
    def Add to cart button for Sauce Labs Bike Light(self):
        """Button to add the Sauce Labs Bike Light to the shopping cart."""
        return self.page.[data-test='add-to-cart-sauce-labs-bike-light'].or_(self.page.text='Add to cart')

    @property
    def Add to cart button for Sauce Labs Bolt T-Shirt(self):
        """Button to add the Sauce Labs Bolt T-Shirt to the shopping cart."""
        return self.page.[data-test='add-to-cart-sauce-labs-bolt-t-shirt'].or_(self.page.text='Add to cart')

    @property
    def Add to cart button for Sauce Labs Fleece Jacket(self):
        """Button to add the Sauce Labs Fleece Jacket to the shopping cart."""
        return self.page.[data-test='add-to-cart-sauce-labs-fleece-jacket'].or_(self.page.text='Add to cart')

    @property
    def Add to cart button for Sauce Labs Onesie(self):
        """Button to add the Sauce Labs Onesie to the shopping cart."""
        return self.page.[data-test='add-to-cart-sauce-labs-onesie'].or_(self.page.text='Add to cart')

    @property
    def Add to cart button for Test.allTheThings() T-Shirt (Red)(self):
        """Button to add the Test.allTheThings() T-Shirt (Red) to the shopping cart."""
        return self.page.[data-test='add-to-cart-test.allthethings()-t-shirt-(red)'].or_(self.page.text='Add to cart')

    @property
    def Shopping Cart Icon(self):
        """Link to navigate to the shopping cart page."""
        return self.page.css=.shopping_cart_link.or_(self.page.role=img[alt='Open Menu'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Product sort dropdown is displayed
        await At least one product item is displayed