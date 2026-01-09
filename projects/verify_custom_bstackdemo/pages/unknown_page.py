from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the main product listing page of the BrowserStack Demo website, displaying available products and allowing users to add them to their cart. The screenshot also shows the shopping cart modal.
    URL Pattern: https://bstackdemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Apple Filter(self):
        """Button to filter products by Apple."""
        return self.page.role=button[name="Apple"].or_(self.page.text=Apple)

    @property
    def Samsung Filter(self):
        """Button to filter products by Samsung."""
        return self.page.role=button[name="Samsung"].or_(self.page.text=Samsung)

    @property
    def Google Filter(self):
        """Button to filter products by Google."""
        return self.page.role=button[name="Google"].or_(self.page.text=Google)

    @property
    def OnePlus Filter(self):
        """Button to filter products by OnePlus."""
        return self.page.role=button[name="OnePlus"].or_(self.page.text=OnePlus)

    @property
    def Add to cart (iPhone 12)(self):
        """Button to add the iPhone 12 to the cart."""
        return self.page.role=button[name="Add to cart"].or_(self.page.text=Add to cart)

    @property
    def Add to cart (iPhone 12 Mini)(self):
        """Button to add the iPhone 12 Mini to the cart."""
        return self.page.role=button[name="Add to cart"].or_(self.page.text=Add to cart)

    @property
    def Bag Icon(self):
        """Icon to open the shopping cart."""
        return self.page.role=button[name="1"].or_(self.page.css=svg[aria-label="1"])

    @property
    def Checkout Button(self):
        """Button to proceed to checkout."""
        return self.page.role=button[name="Checkout"].or_(self.page.text=CHECKOUT)

    @property
    def Remove Item from Cart(self):
        """Button to remove an item from the cart."""
        return self.page.role=button[name="remove"].or_(self.page.css=.float-right.close-item)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'BrowserStack Demo'
        await Page contains the text 'Shop smarter with our mobile e-commerce platform!'
        await At least one product is displayed on the page
        await The 'Bag' modal is displayed