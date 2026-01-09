from playwright.async_api import Page, expect

class LoginPage:
    """
    This page is the Login page for the DemoQA website, allowing users to log in to the Book Store application.
    URL Pattern: https://demoqa.com/login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for entering the username."""
        return self.page.//label[text()='UserName :']/following-sibling::input.or_(self.page.input#userName)

    @property
    def Password Input(self):
        """Input field for entering the password."""
        return self.page.//label[text()='Password :']/following-sibling::input.or_(self.page.input#password)

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.button#login.or_(self.page.//button[@id='login'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'DEMOQA'
        await Page contains the 'Login' heading
        await Page contains the 'UserName' label
        await Page contains the 'Password' label
        await Page contains the 'Login' button