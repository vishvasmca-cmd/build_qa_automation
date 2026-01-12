from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    This page displays the inventory of products available for purchase on the Saucedemo website.
    URL Pattern: https://www.saucedemo.com/inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_name(self):
        """The name of the product, which links to the product details page."""
        return self.page.[class*='inventory_item_name'].or_(self.page.css=.inventory_item_label a div)

    @property
    def product_description(self):
        """The description of the product."""
        return self.page.[class*='inventory_item_desc'].or_(self.page.css=.inventory_item_label div.inventory_item_desc)

    @property
    def product_price(self):
        """The price of the product."""
        return self.page.[class*='inventory_item_price'].or_(self.page.css=.inventory_item_pricebar div.inventory_item_price)

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.[class*='btn_inventory'].or_(self.page.text=Add to cart)

    @property
    def remove_button(self):
        """Button to remove the product from the shopping cart."""
        return self.page.[class*='btn_inventory'].or_(self.page.text=Remove)

    @property
    def products_header(self):
        """The header text indicating the page displays products."""
        return self.page.text=Products.or_(self.page.css=.title)

    @property
    def filter_sort_dropdown(self):
        """Dropdown to filter or sort the products."""
        return self.page.data-test=product_sort_container.or_(self.page.css=[data-test='product_sort_container'])

    @property
    def shopping_cart_link(self):
        """Link to the shopping cart page."""
        return self.page.id=shopping_cart_container.or_(self.page.css=a.shopping_cart_link)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Swag Labs'
        await Page contains a header with the text 'Products'
        await At least one product item is displayed on the page
        await The 'Add to cart' button is visible for products not in the cart
        await The 'Remove' button is visible for products already in the cart