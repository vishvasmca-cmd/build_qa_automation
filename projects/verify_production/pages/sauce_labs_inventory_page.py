from playwright.async_api import Page, expect

class SauceLabsInventoryPage:
    """
    Inventory page displaying a list of products available for purchase.
    URL Pattern: /inventory
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def product_label(self):
        """Label indicating the page displays products."""
        return self.page.get_by_text("Products").or_(self.page.locator(".title"))

    @property
    def product_item(self):
        """Individual product item in the inventory list."""
        return self.page.locator(".inventory_item").or_(self.page.locator(".inventory_list > div"))

    @property
    def product_image(self):
        """Image associated with a product."""
        return self.page.locator(".inventory_item_img img").or_(self.page.locator(".inventory_item_img a"))

    @property
    def product_name(self):
        """Name of the product, usually a link to the product details page."""
        return self.page.locator(".inventory_item_name").or_(self.page.locator(".inventory_item_description a"))

    @property
    def product_description(self):
        """Description of the product."""
        return self.page.locator(".inventory_item_desc").or_(self.page.locator(".inventory_item_description > div"))

    @property
    def product_price(self):
        """Price of the product."""
        return self.page.locator(".inventory_item_price").or_(self.page.locator(".inventory_item_description > div.inventory_item_price"))

    @property
    def add_to_cart_button(self):
        """Button to add the product to the shopping cart."""
        return self.page.locator("button:has-text('Add to cart')").or_(self.page.locator("button[id^='add-to-cart']"))

    @property
    def remove_button(self):
        """Button to remove the product from the shopping cart."""
        return self.page.locator("button:has-text('Remove')").or_(self.page.locator("button[id^='remove']"))

    @property
    def shopping_cart_link(self):
        """Link to navigate to the shopping cart page."""
        return self.page.locator(".shopping_cart_link").or_(self.page.locator("#shopping_cart_container a"))

    @property
    def menu_button(self):
        """Button to open the side menu."""
        return self.page.locator("#react-burger-menu-btn").or_(self.page.locator("#menu_button"))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_url('https://www.saucedemo.com/inventory.html')
        await expect(page.get_by_text('Products')).to_be_visible()
        await expect(page.locator(".inventory_item")).to_have_count(6)