from playwright.async_api import Page, expect

class HomePage:
    """
    The home page of the BrowserStack Demo e-commerce website, displaying a catalog of phones.
    URL Pattern: https://bstackdemo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def BrowserStack Logo(self):
        """Link to the home page."""
        return self.page.role=link[name="BrowserStack"].or_(self.page.css=.Navbar_logo__26S5Y)

    @property
    def Search Input(self):
        """Input field for searching products."""
        return self.page.role=searchbox[name="Search"].or_(self.page.css=#search-input)

    @property
    def Search Button(self):
        """Button to initiate the search."""
        return self.page.role=button[name="Search"].or_(self.page.css=#search-button)

    @property
    def Sign In(self):
        """Link to the sign-in page."""
        return self.page.role=button[name="Sign In"].or_(self.page.text=Sign In)

    @property
    def Cart(self):
        """Button to view the shopping cart."""
        return self.page.role=button[name="0"].or_(self.page.css=.MuiButtonBase-root.e-commerce_header-bag__2K2Xn)

    @property
    def Apple Filter(self):
        """Filter products by Apple vendor."""
        return self.page.role=button[name="Apple"].or_(self.page.text=Apple)

    @property
    def Samsung Filter(self):
        """Filter products by Samsung vendor."""
        return self.page.role=button[name="Samsung"].or_(self.page.text=Samsung)

    @property
    def Google Filter(self):
        """Filter products by Google vendor."""
        return self.page.role=button[name="Google"].or_(self.page.text=Google)

    @property
    def OnePlus Filter(self):
        """Filter products by OnePlus vendor."""
        return self.page.role=button[name="OnePlus"].or_(self.page.text=OnePlus)

    @property
    def Order By Select(self):
        """Dropdown to select the order of products."""
        return self.page.role=button[name="Select"].or_(self.page.text=Select)

    @property
    def Add to cart(self):
        """Button to add the product to the cart."""
        return self.page.role=button[name="Add to cart"].or_(self.page.text=Add to cart)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'BrowserStack Demo'
        await Page contains the text 'Shop smarter with our mobile e-commerce platform!'
        await At least one product is displayed on the page.