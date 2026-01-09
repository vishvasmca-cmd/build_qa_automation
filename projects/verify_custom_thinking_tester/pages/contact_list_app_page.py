from playwright.async_api import Page, expect

class ContactListAppPage:
    """
    This is the Login page for the Contact List App. It allows existing users to log in with their email and password, and provides a link for new users to sign up.
    URL Pattern: https://thinking-tester-contact-list.herokuapp.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Email Input(self):
        """Input field for entering the user's email address."""
        return self.page.role=textbox[name="email"].or_(self.page.css=input[id="email"])

    @property
    def Password Input(self):
        """Input field for entering the user's password."""
        return self.page.role=textbox[name="password"].or_(self.page.css=input[id="password"])

    @property
    def Submit Button(self):
        """Button to submit the login form."""
        return self.page.role=button[name="Submit"].or_(self.page.css=button[id="submit"])

    @property
    def Sign Up Link(self):
        """Link to navigate to the sign-up page for new users."""
        return self.page.role=button[name="Sign up"].or_(self.page.text=Sign up)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Contact List App'
        await Header text is 'Contact List App'
        await Email input field is present
        await Password input field is present
        await Submit button is present
        await Sign up link is present