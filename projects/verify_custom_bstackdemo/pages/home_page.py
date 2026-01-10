from playwright.async_api import Page, expect

class HomePage:
    """
    The home page of the BrowserStack demo application, showcasing available products.
    URL Pattern: https://bstackdemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Input(self):
        """Input field for searching products."""
        return self.page.role=searchbox.or_(self.page.css=input[type='text'])

    @property
    def Search Button(self):
        """Button to trigger the search."""
        return self.page.text=Search.or_(self.page.css=#search > span)

    @property
    def Sign In Link(self):
        """Link to the sign-in page."""
        return self.page.text=Sign In.or_(self.page.css=#signin)

    @property
    def Apple Filter(self):
        """Filter button to show Apple products."""
        return self.page.text=Apple.or_(self.page.css=#apple)

    @property
    def Samsung Filter(self):
        """Filter button to show Samsung products."""
        return self.page.text=Samsung.or_(self.page.css=#samsung)

    @property
    def Google Filter(self):
        """Filter button to show Google products."""
        return self.page.text=Google.or_(self.page.css=#google)

    @property
    def OnePlus Filter(self):
        """Filter button to show OnePlus products."""
        return self.page.text=OnePlus.or_(self.page.css=#oneplus)

    @property
    def Add to cart button for iPhone 12(self):
        """Button to add the iPhone 12 to the cart."""
        return self.page.text=Add to cart.or_(self.page.css=div:nth-child(1) > div > div.shelf-item__buy-btn > div)

    @property
    def Add to cart button for iPhone 12 Mini(self):
        """Button to add the iPhone 12 Mini to the cart."""
        return self.page.text=Add to cart.or_(self.page.css=div:nth-child(2) > div > div.shelf-item__buy-btn > div)

    @property
    def Bag Icon(self):
        """Button to open the shopping cart."""
        return self.page.text=Bag.or_(self.page.css=#__next > div > div > div.MuiBox-root.css-10ifv83 > div.MuiBox-root.css-k008qs > div.float-cart__content > div.float-cart__header > span)

    @property
    def Checkout Button(self):
        """Button to proceed to checkout."""
        return self.page.text=CHECKOUT.or_(self.page.css=#__next > div > div > div.MuiBox-root.css-10ifv83 > div.MuiBox-root.css-k008qs > div.float-cart__content > div.float-cart__footer > button)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'BrowserStack Demo'
        await Page contains the header 'Shop smarter with our mobile e-commerce platform!'
        await At least one product is displayed on the page
        await The 'Bag' icon is visible