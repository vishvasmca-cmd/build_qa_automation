from playwright.async_api import Page, expect

class AddUserPage:
    """
    This page allows a user to create a new contact by providing their details such as name, email, and password.
    URL Pattern: https://thinking-tester-contact-list.herokuapp.com/addUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def First Name Input(self):
        """Input field for the user's first name."""
        return self.page.role=textbox[name="firstName"].or_(self.page.css=input[id="firstName"])

    @property
    def Last Name Input(self):
        """Input field for the user's last name."""
        return self.page.role=textbox[name="lastName"].or_(self.page.css=input[id="lastName"])

    @property
    def Email Input(self):
        """Input field for the user's email address."""
        return self.page.role=textbox[name="email"].or_(self.page.css=input[id="email"])

    @property
    def Password Input(self):
        """Input field for the user's password."""
        return self.page.role=textbox[name="password"].or_(self.page.css=input[id="password"])

    @property
    def Submit Button(self):
        """Button to submit the new user form."""
        return self.page.role=button[name="Submit"].or_(self.page.text=Submit)

    @property
    def Cancel Button(self):
        """Button to cancel the new user creation and navigate back."""
        return self.page.role=button[name="Cancel"].or_(self.page.text=Cancel)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Add User'
        await Header text 'Add User' is present
        await All input fields (First Name, Last Name, Email, Password) are visible
        await Submit and Cancel buttons are visible