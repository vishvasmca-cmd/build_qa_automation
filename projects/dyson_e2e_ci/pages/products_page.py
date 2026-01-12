from playwright.async_api import Page, expect

class ProductsPage:
    """
    This page displays an 'Access Denied' error, indicating that the user does not have permission to access the requested resource (adding a product to the cart).
    URL Pattern: https://www.dyson.in/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZHlzb24uaW4vYWlyc3RyYWl0LWhhaXItc3RyYWlnaHRlbmVyLXBpbmstZ29sZA~~/product/69594/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def access_denied_heading(self):
        """The main heading indicating access is denied."""
        return self.page.text=Access Denied.or_(self.page.h1:contains('Access Denied'))

    @property
    def error_description(self):
        """The paragraph explaining the access denial."""
        return self.page.text=You don't have permission to access.or_(self.page.p:contains('You don\'t have permission to access'))

    @property
    def error_url(self):
        """Link to the error details page."""
        return self.page.text=https://errors.edgesuite.net/18.c969dc17.1768252189.1e2cb7e9.or_(self.page.a[href='https://errors.edgesuite.net/18.c969dc17.1768252189.1e2cb7e9'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Access Denied'
        await Verify that the 'Access Denied' heading is displayed
        await Verify that the error description is displayed
        await Verify that the error URL is displayed