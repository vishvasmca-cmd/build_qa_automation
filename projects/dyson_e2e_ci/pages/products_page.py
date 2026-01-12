from playwright.async_api import Page, expect

class ProductsPage:
    """
    This page indicates an 'Access Denied' error when trying to add a product to the cart. The user does not have permission to access the specified URL.
    URL Pattern: http://www.dyson.in/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZHlzb24uaW4vYWlyd3JhcC1vcmlnaW4tbmlja2VsLWNvcHBlcg%7e%7e/product/71588/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def access_denied_header(self):
        """The main header indicating access is denied."""
        return self.page.role=heading[name="Access Denied"].or_(self.page.text="Access Denied")

    @property
    def error_description(self):
        """The description explaining the reason for the error."""
        return self.page.text="You don't have permission to access".or_(self.page.text="You don't have permission to access")

    @property
    def error_url(self):
        """The URL that the user is trying to access."""
        return self.page.text="http://www.dyson.in/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZHlzb24uaW4vYWlyd3JhcC1vcmlnaW4tbmlja2VsLWNvcHBlcg%7e%7e/product/71588/".or_(self.page.text="http://www.dyson.in/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZHlzb24uaW4vYWlyd3JhcC1vcmlnaW4tbmlja2VsLWNvcHBlcg%7e%7e/product/71588/")

    @property
    def reference_number(self):
        """The reference number for the error."""
        return self.page.text="Reference #18.253b2f17.1768195387.39aa67d6".or_(self.page.text="Reference #18.253b2f17.1768195387.39aa67d6")

    @property
    def edgesuite_url(self):
        """The URL for the edgesuite error page."""
        return self.page.text="https://errors.edgesuite.net/18.253b2f17.1768195387.39aa67d6".or_(self.page.text="https://errors.edgesuite.net/18.253b2f17.1768195387.39aa67d6")

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Access Denied'
        await Verify that the 'Access Denied' header is displayed
        await Verify that the error description is displayed
        await Verify that the error URL is displayed
        await Verify that the reference number is displayed
        await Verify that the edgesuite URL is displayed