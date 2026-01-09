from playwright.async_api import Page, expect

class LoginPagePage:
    """
    This is the Login Page for the-internet.herokuapp.com/secure. It allows users to enter their username and password to access the secure area.
    URL Pattern: https://the-internet.herokuapp.com/secure
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for the username."""
        return self.page.//label[text()='Username']/following-sibling::input.or_(self.page.input#username)

    @property
    def Password Input(self):
        """Input field for the password."""
        return self.page.//label[text()='Password']/following-sibling::input.or_(self.page.input#password)

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.//button[@class='radius'].or_(self.page.button[type='submit'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'The Internet'
        await Page heading is 'Login Page'
        await Username input field is present
        await Password input field is present
        await Login button is present