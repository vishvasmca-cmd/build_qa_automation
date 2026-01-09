from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page indicates an issue with the website's SSL certificate.
    URL Pattern: https://magento.softwaretestingboard.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Invalid SSL certificate Header(self):
        """The main header indicating the SSL certificate issue."""
        return self.page.text=Invalid SSL certificate.or_(self.page.h1)

    @property
    def Error Code(self):
        """Error code associated with the SSL issue."""
        return self.page.text=Error code 526.or_(self.page.Error code 526)

    @property
    def Cloudflare Link(self):
        """Link to Cloudflare for more information."""
        return self.page.text=cloudflare.com.or_(self.page.a[href='cloudflare.com'])

    @property
    def Browser Status(self):
        """Indicates the browser is working correctly."""
        return self.page.text=Browser Working.or_(self.page.text=Browser Working)

    @property
    def Cloudflare Status(self):
        """Indicates Cloudflare is working correctly."""
        return self.page.text=Cloudflare Working.or_(self.page.text=Cloudflare Working)

    @property
    def Host Error(self):
        """Indicates an error with the host."""
        return self.page.text=Host Error.or_(self.page.text=Host Error)

    @property
    def What happened?(self):
        """Section header explaining the SSL issue."""
        return self.page.text=What happened?.or_(self.page.text=What happened?)

    @property
    def What can I do?(self):
        """Section header providing possible solutions."""
        return self.page.text=What can I do?.or_(self.page.text=What can I do?)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Invalid SSL certificate'
        await Header 'Invalid SSL certificate' is displayed
        await Text 'Error code 526' is displayed
        await Text 'The origin web server does not have a valid SSL certificate.' is displayed