from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the products page where users can view and search for available products.
    URL Pattern: https://automationexercise.com/products
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Search Product Input(self):
        """Input field to enter the product name to search for."""
        return self.page.//input[@id='search_product'].or_(self.page.css=input#search_product)

    @property
    def Search Product Button(self):
        """Button to submit the product search."""
        return self.page.//button[@id='submit_search'].or_(self.page.css=button#submit_search)

    @property
    def Category Women(self):
        """Category filter button for Women."""
        return self.page.//div[@id='accordian']/div[1]/div[1]/h4/a.or_(self.page.text=Women)

    @property
    def Category Men(self):
        """Category filter button for Men."""
        return self.page.//div[@id='accordian']/div[2]/div[1]/h4/a.or_(self.page.text=Men)

    @property
    def Category Kids(self):
        """Category filter button for Kids."""
        return self.page.//div[@id='accordian']/div[3]/div[1]/h4/a.or_(self.page.text=Kids)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Verify that the page title is 'Automation Exercise - All Products'
        await Verify that the 'ALL PRODUCTS' text is displayed.
        await Verify that the search input field is present.