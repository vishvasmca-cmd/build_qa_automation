from playwright.async_api import Page, expect

class HomePage:
    """
    This is the home page of the Swag Labs e-commerce website, displaying a list of available products.
    URL Pattern: https://www.saucedemo.com/
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
    def Add to Cart Button(self):
        """Button to add the product to the shopping cart."""
        return self.page.//button[contains(text(),'Add to cart')].or_(self.page.button:contains('Add to cart'))

    @property
    def Shopping Cart Icon(self):
        """Link to the shopping cart page."""
        return self.page.[data-icon='shopping-cart'].or_(self.page..shopping_cart_link)

    @property
    def Product Sort Container(self):
        """Dropdown to sort the products."""
        return self.page.[data-test='product_sort_container'].or_(self.page..product_sort_container)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await At least one product is displayed
        await The 'Add to cart' button is visible for each product