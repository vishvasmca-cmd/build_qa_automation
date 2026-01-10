from playwright.async_api import Page, expect

class HomePage:
    """
    The home page of the BrowserStack demo website, showcasing available products and allowing users to add them to the cart.
    URL Pattern: https://bstackdemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Apple Filter(self):
        """Filter products by Apple vendor."""
        return self.page.data-testid=Apple.or_(self.page.text=Apple)

    @property
    def Samsung Filter(self):
        """Filter products by Samsung vendor."""
        return self.page.data-testid=Samsung.or_(self.page.text=Samsung)

    @property
    def Google Filter(self):
        """Filter products by Google vendor."""
        return self.page.data-testid=Google.or_(self.page.text=Google)

    @property
    def OnePlus Filter(self):
        """Filter products by OnePlus vendor."""
        return self.page.data-testid=OnePlus.or_(self.page.text=OnePlus)

    @property
    def Add to cart button for iPhone 12(self):
        """Button to add the iPhone 12 to the shopping cart."""
        return self.page.data-testid=Add to cart.or_(self.page.//div[contains(text(),'iPhone 12')]/following-sibling::button)

    @property
    def Add to cart button for iPhone 12 Mini(self):
        """Button to add the iPhone 12 Mini to the shopping cart."""
        return self.page.data-testid=Add to cart.or_(self.page.//div[contains(text(),'iPhone 12 Mini')]/following-sibling::button)

    @property
    def Bag Icon(self):
        """Icon to open the shopping cart."""
        return self.page.data-testid=Bag.or_(self.page.css=svg[aria-label='Bag'])

    @property
    def Checkout Button(self):
        """Button to navigate to the checkout page."""
        return self.page.data-testid=Checkout.or_(self.page.text=CHECKOUT)

    @property
    def Search Input(self):
        """Input field for searching products."""
        return self.page.id=search.or_(self.page.css=input[type='text'])

    @property
    def Search Button(self):
        """Button to initiate the search."""
        return self.page.text=Search.or_(self.page.css=button[aria-label='Search'])

    @property
    def Sign In Link(self):
        """Link to navigate to the sign-in page."""
        return self.page.text=Sign In.or_(self.page.css=a[href='/signin'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'BrowserStack Demo'
        await Page contains the text 'Shop smarter with our mobile e-commerce platform!'
        await At least one product is displayed on the page
        await The 'Bag' icon is visible