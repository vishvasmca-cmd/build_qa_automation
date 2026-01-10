from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the inventory page of the Swag Labs demo website, displaying a list of available products.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Sort Dropdown(self):
        """Dropdown to sort the products by name or price."""
        return self.page.data-test="product_sort_container".or_(self.page.#header_container > div.header_secondary_container > div.right_component > span > select)

    @property
    def Add to cart button for Sauce Labs Backpack(self):
        """Button to add the Sauce Labs Backpack to the shopping cart."""
        return self.page.data-test="add-to-cart-sauce-labs-backpack".or_(self.page.div.inventory_item:nth-child(1) > div:nth-child(2) > div:nth-child(2) > button)

    @property
    def Add to cart button for Sauce Labs Bike Light(self):
        """Button to add the Sauce Labs Bike Light to the shopping cart."""
        return self.page.data-test="add-to-cart-sauce-labs-bike-light".or_(self.page.div.inventory_item:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button)

    @property
    def Add to cart button for Sauce Labs Bolt T-Shirt(self):
        """Button to add the Sauce Labs Bolt T-Shirt to the shopping cart."""
        return self.page.data-test="add-to-cart-sauce-labs-bolt-t-shirt".or_(self.page.div.inventory_item:nth-child(3) > div:nth-child(2) > div:nth-child(2) > button)

    @property
    def Add to cart button for Sauce Labs Fleece Jacket(self):
        """Button to add the Sauce Labs Fleece Jacket to the shopping cart."""
        return self.page.data-test="add-to-cart-sauce-labs-fleece-jacket".or_(self.page.div.inventory_item:nth-child(4) > div:nth-child(2) > div:nth-child(2) > button)

    @property
    def Add to cart button for Sauce Labs Onesie(self):
        """Button to add the Sauce Labs Onesie to the shopping cart."""
        return self.page.data-test="add-to-cart-sauce-labs-onesie".or_(self.page.div.inventory_item:nth-child(5) > div:nth-child(2) > div:nth-child(2) > button)

    @property
    def Add to cart button for Test.allTheThings() T-Shirt (Red)(self):
        """Button to add the Test.allTheThings() T-Shirt (Red) to the shopping cart."""
        return self.page.data-test="add-to-cart-test.allthethings()-t-shirt-(red)".or_(self.page.div.inventory_item:nth-child(6) > div:nth-child(2) > div:nth-child(2) > button)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Page contains the 'Products' header
        await At least one product item is displayed