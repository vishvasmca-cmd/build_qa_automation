from playwright.async_api import Page, expect

class ProductsPage:
    """
    This page displays a list of products available on the Automation Exercise website. Users can search for products, filter by category and brand, and view product details.
    URL Pattern: https://www.automationexercise.com/products
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Product Input(self):
        """Input field to search for products."""
        return self.page.//input[@id='search_product'].or_(self.page.input[name='search'])

    @property
    def Search Product Button(self):
        """Button to submit the product search."""
        return self.page.//button[@id='submit_search'].or_(self.page.button[type='button'])

    @property
    def Category Women(self):
        """Link to filter products by Women category."""
        return self.page.//a[text()='Women'].or_(self.page.#accordian > div:nth-child(1) > div.panel-heading > h4 > a)

    @property
    def Category Men(self):
        """Link to filter products by Men category."""
        return self.page.//a[text()='Men'].or_(self.page.#accordian > div:nth-child(2) > div.panel-heading > h4 > a)

    @property
    def Category Kids(self):
        """Link to filter products by Kids category."""
        return self.page.//a[text()='Kids'].or_(self.page.#accordian > div:nth-child(3) > div.panel-heading > h4 > a)

    @property
    def Products Link(self):
        """Link to the products page in the header."""
        return self.page.//a[text()=' Products'].or_(self.page.li:nth-child(2) > a)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify page title contains 'Automation Exercise - All Products'
        await Verify 'ALL PRODUCTS' header is visible
        await Verify at least one product is displayed