from playwright.async_api import Page, expect

class AddUserPage:
    """
    This page allows a user to create a new account by providing their first name, last name, email, and password.
    URL Pattern: https://thinking-tester-contact-list.herokuapp.com/addUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def First Name Input(self):
        """Input field for the user's first name."""
        return self.page.id=firstName.or_(self.page.css=input[id='firstName'])

    @property
    def Last Name Input(self):
        """Input field for the user's last name."""
        return self.page.id=lastName.or_(self.page.css=input[id='lastName'])

    @property
    def Email Input(self):
        """Input field for the user's email address."""
        return self.page.id=email.or_(self.page.css=input[id='email'])

    @property
    def Password Input(self):
        """Input field for the user's password."""
        return self.page.id=password.or_(self.page.css=input[id='password'])

    @property
    def Submit Button(self):
        """Button to submit the new user form."""
        return self.page.id=submit.or_(self.page.css=button[id='submit'])

    @property
    def Cancel Button(self):
        """Button to cancel the new user creation and navigate back."""
        return self.page.id=cancel.or_(self.page.css=button[id='cancel'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Add User'
        await Header text is 'Add User'
        await The 'Sign up to begin adding your contacts!' text is present