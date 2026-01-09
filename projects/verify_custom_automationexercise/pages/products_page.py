from playwright.async_api import Page, expect

class ProductsPage:
    """
    This page displays a list of products available on the Automation Exercise website.
    URL Pattern: https://automationexercise.com/products
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
        return self.page.//button[@id='submit_search'].or_(self.page.button[class='btn btn-default search'])

    @property
    def Category Women(self):
        """Category filter for Women."""
        return self.page.//div[@id='accordian']/div[1]/div[1]/h4/a.or_(self.page.#accordian > div:nth-child(1) > div.panel-heading > h4 > a)

    @property
    def Category Men(self):
        """Category filter for Men."""
        return self.page.//div[@id='accordian']/div[2]/div[1]/h4/a.or_(self.page.#accordian > div:nth-child(2) > div.panel-heading > h4 > a)

    @property
    def Category Kids(self):
        """Category filter for Kids."""
        return self.page.//div[@id='accordian']/div[3]/div[1]/h4/a.or_(self.page.#accordian > div:nth-child(3) > div.panel-heading > h4 > a)

    @property
    def Products Link(self):
        """Link to the products page in the header."""
        return self.page.//a[text()=' Products'].or_(self.page.a[href='/products'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the page title contains 'Automation Exercise - All Products'
        await Verify that the 'ALL PRODUCTS' header is displayed
        await Verify that product listings are displayed