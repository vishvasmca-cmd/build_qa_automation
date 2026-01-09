from playwright.async_api import Page, expect

class SwagLabsPage:
    """
    Inventory page displaying available products.
    URL Pattern: /inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_name(self):
        """Name of the product"""
        return self.page.get_by_role('link', name=re.compile(r'\w+', re.IGNORECASE)).or_(self.page.locator('.inventory_item_name'))

    @property
    def product_description(self):
        """Description of the product"""
        return self.page.locator('.inventory_item_desc').or_(self.page.locator('.inventory_item_label > div:nth-child(2)'))

    @property
    def product_price(self):
        """Price of the product"""
        return self.page.locator('.inventory_item_price').or_(self.page.locator('.inventory_item_label > div:nth-child(3)'))

    @property
    def add_to_cart_button(self):
        """Button to add the product to the cart"""
        return self.page.get_by_role('button', name=re.compile(r'Add to cart', re.IGNORECASE)).or_(self.page.locator('[data-test^="add-to-cart-"]'))

    @property
    def remove_from_cart_button(self):
        """Button to remove the product from the cart"""
        return self.page.get_by_role('button', name=re.compile(r'Remove', re.IGNORECASE)).or_(self.page.locator('[data-test^="remove-"]'))

    @property
    def shopping_cart_link(self):
        """Link to the shopping cart"""
        return self.page.locator('#shopping_cart_container > a').or_(self.page.locator('.shopping_cart_link'))

    @property
    def menu_button(self):
        """Button to open the side menu"""
        return self.page.locator('#react-burger-menu-btn').or_(self.page.locator('#menu_button'))

    @property
    def product_sort_container(self):
        """Dropdown to sort products"""
        return self.page.locator('[data-test="product_sort_container"]').or_(self.page.locator('.product_sort_container'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Swag Labs')
        await expect(page.locator('.title')).to_have_text('Products')
        await expect(page.url).to_contain('/inventory.html')