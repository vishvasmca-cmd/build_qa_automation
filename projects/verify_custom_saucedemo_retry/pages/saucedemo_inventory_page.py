from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    This page displays the inventory of products available for purchase on the Saucedemo website.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Product Name(self):
        """The name of the product, which is a link to the product details page."""
        return self.page.//div[@class='inventory_item_label']/a/div[@class='inventory_item_name '].or_(self.page..inventory_item_name)

    @property
    def Product Description(self):
        """The description of the product."""
        return self.page.//div[@class='inventory_item_label']/div[@class='inventory_item_desc'].or_(self.page..inventory_item_desc)

    @property
    def Product Price(self):
        """The price of the product."""
        return self.page.//div[@class='inventory_item_price'].or_(self.page..inventory_item_price)

    @property
    def Add to Cart Button(self):
        """Button to add the product to the shopping cart."""
        return self.page.//button[contains(@id, 'add-to-cart')].or_(self.page.button[class='btn btn_primary btn_small btn_inventory'])

    @property
    def Remove Button(self):
        """Button to remove the product from the shopping cart."""
        return self.page.//button[contains(@id, 'remove')].or_(self.page.button[class='btn btn_secondary btn_small btn_inventory'])

    @property
    def Products Header(self):
        """The header text indicating the page displays products."""
        return self.page.//span[text()='Products'].or_(self.page..title)

    @property
    def Filter/Sort Dropdown(self):
        """Dropdown to filter or sort the products."""
        return self.page.//select[@class='product_sort_container'].or_(self.page..product_sort_container)

    @property
    def Shopping Cart Link(self):
        """Link to the shopping cart page."""
        return self.page.//a[@class='shopping_cart_link'].or_(self.page..shopping_cart_link)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await The 'Products' header is displayed
        await At least one product is displayed on the page
        await The 'Add to Cart' button is displayed for each product
        await The filter/sort dropdown is displayed