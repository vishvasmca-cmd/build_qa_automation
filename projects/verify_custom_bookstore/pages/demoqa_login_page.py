from playwright.async_api import Page, expect

class DemoqaLoginPage:
    """
    This page is the login page for the DemoQA bookstore application, where users can enter their credentials to access their accounts.
    URL Pattern: https://demoqa.com/login
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for entering the username."""
        return self.page.//label[text()='UserName :']/following-sibling::input.or_(self.page.#userName)

    @property
    def Password Input(self):
        """Input field for entering the password."""
        return self.page.//label[text()='Password :']/following-sibling::input.or_(self.page.#password)

    @property
    def Login Button(self):
        """Button to submit the login form."""
        return self.page.#login.or_(self.page.//button[@id='login'])

    @property
    def New User Button(self):
        """Button to navigate to the registration page for new users."""
        return self.page.//button[text()='New User'].or_(self.page.//button[@id='newUser'])

    @property
    def Invalid username or password message(self):
        """Error message displayed when login fails."""
        return self.page.#name.or_(self.page.//p[@id='name'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'DEMOQA'
        await The header text 'Login' is displayed.
        await The 'Username' input field is present.
        await The 'Password' input field is present.
        await The 'Login' button is present.
        await The 'New User' button is present.