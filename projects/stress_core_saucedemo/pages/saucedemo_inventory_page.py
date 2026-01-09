from playwright.async_api import Page, expect

class SaucedemoInventoryPage:
    """
    Inventory page displaying available products
    URL Pattern: /inventory.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_sort_dropdown(self):
        """Dropdown to sort products"""
        return self.page.get_by_role('button', name='Name (A to Z)').or_(self.page.locator('[data-test="product_sort_container"]'))

    @property
    def add_to_cart_backpack(self):
        """Add to cart button for the Sauce Labs Backpack"""
        return self.page.get_by_role('button', name='Add to cart', exact=True).nth(0).or_(self.page.locator('#add-to-cart-sauce-labs-backpack'))

    @property
    def add_to_cart_bike_light(self):
        """Add to cart button for the Sauce Labs Bike Light"""
        return self.page.get_by_role('button', name='Add to cart', exact=True).nth(1).or_(self.page.locator('#add-to-cart-sauce-labs-bike-light'))

    @property
    def add_to_cart_bolt_tshirt(self):
        """Add to cart button for the Sauce Labs Bolt T-Shirt"""
        return self.page.get_by_role('button', name='Add to cart', exact=True).nth(2).or_(self.page.locator('#add-to-cart-sauce-labs-bolt-t-shirt'))

    @property
    def add_to_cart_fleece_jacket(self):
        """Add to cart button for the Sauce Labs Fleece Jacket"""
        return self.page.get_by_role('button', name='Add to cart', exact=True).nth(3).or_(self.page.locator('#add-to-cart-sauce-labs-fleece-jacket'))

    @property
    def add_to_cart_onesie(self):
        """Add to cart button for the Sauce Labs Onesie"""
        return self.page.get_by_role('button', name='Add to cart', exact=True).nth(4).or_(self.page.locator('#add-to-cart-sauce-labs-onesie'))

    @property
    def add_to_cart_red_tshirt(self):
        """Add to cart button for the Test.allTheThings() T-Shirt (Red)"""
        return self.page.get_by_role('button', name='Add to cart', exact=True).nth(5).or_(self.page.locator('#add-to-cart-test.allthethings()-t-shirt-(red)'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Swag Labs')
        await expect(page.locator('.title')).to_have_text('Products')
        await expect(page.locator('.inventory_item')).to_have_count(6)