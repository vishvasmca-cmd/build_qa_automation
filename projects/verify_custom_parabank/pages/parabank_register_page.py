from playwright.async_api import Page, expect

class ParabankRegisterPage:
    """
    This page allows new users to register for an account with ParaBank.
    URL Pattern: https://parabank.parasoft.com/parabank/register.htm*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name(self):
        """Input field for the user's first name."""
        return self.page.id=customer.firstName.or_(self.page.css=input[name='customer.firstName'])

    @property
    def last_name(self):
        """Input field for the user's last name."""
        return self.page.id=customer.lastName.or_(self.page.css=input[name='customer.lastName'])

    @property
    def address(self):
        """Input field for the user's address."""
        return self.page.id=customer.address.street.or_(self.page.css=input[name='customer.address.street'])

    @property
    def city(self):
        """Input field for the user's city."""
        return self.page.id=customer.address.city.or_(self.page.css=input[name='customer.address.city'])

    @property
    def state(self):
        """Input field for the user's state."""
        return self.page.id=customer.address.state.or_(self.page.css=input[name='customer.address.state'])

    @property
    def zip_code(self):
        """Input field for the user's zip code."""
        return self.page.id=customer.address.zipCode.or_(self.page.css=input[name='customer.address.zipCode'])

    @property
    def phone(self):
        """Input field for the user's phone number."""
        return self.page.id=customer.phoneNumber.or_(self.page.css=input[name='customer.phoneNumber'])

    @property
    def ssn(self):
        """Input field for the user's social security number."""
        return self.page.id=customer.ssn.or_(self.page.css=input[name='customer.ssn'])

    @property
    def username(self):
        """Input field for the user's desired username."""
        return self.page.id=customer.username.or_(self.page.css=input[name='customer.username'])

    @property
    def password(self):
        """Input field for the user's desired password."""
        return self.page.id=customer.password.or_(self.page.css=input[name='customer.password'])

    @property
    def confirm(self):
        """Input field to confirm the user's password."""
        return self.page.id=repeatedPassword.or_(self.page.css=input[name='repeatedPassword'])

    @property
    def register(self):
        """Button to submit the registration form."""
        return self.page.css=input[value='Register'].or_(self.page.value=Register)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ParaBank | Register'
        await Header text contains 'Signing up is easy!'
        await The 'First Name' input field is present
        await The 'Register' button is present