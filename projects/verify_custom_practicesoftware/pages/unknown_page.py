from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page is for user login and registration.
    URL Pattern: https://practice.automationtesting.in/my-account/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username or email address input(self):
        """Input field for username or email address for login."""
        return self.page.//label[text()='Username or email address *']/following-sibling::input.or_(self.page.css:#username)

    @property
    def Password input (Login)(self):
        """Password input field for login."""
        return self.page.//label[text()='Password *']/following-sibling::input[@type='password'].or_(self.page.css:#password)

    @property
    def Login button(self):
        """Button to submit the login form."""
        return self.page.//input[@name='login'].or_(self.page.css:input[value='Login'])

    @property
    def Remember me checkbox(self):
        """Checkbox to remember the user's login details."""
        return self.page.//label[text()='Remember me']/input[@type='checkbox'].or_(self.page.css:#rememberme)

    @property
    def Lost your password link(self):
        """Link to navigate to the password reset page."""
        return self.page.//a[text()='Lost your password?'].or_(self.page.css:a[href*='lost-password'])

    @property
    def Email address input (Register)(self):
        """Input field for email address for registration."""
        return self.page.//label[text()='Email address *']/following-sibling::input.or_(self.page.css:#reg_email)

    @property
    def Password input (Register)(self):
        """Password input field for registration."""
        return self.page.//label[text()='Password *']/following-sibling::input[@type='password'].or_(self.page.css:#reg_password)

    @property
    def Register button(self):
        """Button to submit the registration form."""
        return self.page.//input[@name='register'].or_(self.page.css:input[value='Register'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'My Account'
        await Presence of 'Login' heading
        await Presence of 'Register' heading
        await Login button is present
        await Register button is present