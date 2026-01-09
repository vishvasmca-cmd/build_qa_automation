from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the registration page where new users can create an account.
    URL Pattern: https://parabank.parasoft.com/parabank/register.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def First Name(self):
        """Input field for the user's first name."""
        return self.page.id=customer.firstName.or_(self.page.css=input[name='customer.firstName'])

    @property
    def Last Name(self):
        """Input field for the user's last name."""
        return self.page.id=customer.lastName.or_(self.page.css=input[name='customer.lastName'])

    @property
    def Address(self):
        """Input field for the user's address."""
        return self.page.id=customer.address.street.or_(self.page.css=input[name='customer.address.street'])

    @property
    def City(self):
        """Input field for the user's city."""
        return self.page.id=customer.address.city.or_(self.page.css=input[name='customer.address.city'])

    @property
    def State(self):
        """Input field for the user's state."""
        return self.page.id=customer.address.state.or_(self.page.css=input[name='customer.address.state'])

    @property
    def Zip Code(self):
        """Input field for the user's zip code."""
        return self.page.id=customer.address.zipCode.or_(self.page.css=input[name='customer.address.zipCode'])

    @property
    def Phone Number(self):
        """Input field for the user's phone number."""
        return self.page.id=customer.phoneNumber.or_(self.page.css=input[name='customer.phoneNumber'])

    @property
    def SSN(self):
        """Input field for the user's social security number."""
        return self.page.id=customer.ssn.or_(self.page.css=input[name='customer.ssn'])

    @property
    def Username(self):
        """Input field for the user's desired username."""
        return self.page.id=customer.username.or_(self.page.css=input[name='customer.username'])

    @property
    def Password(self):
        """Input field for the user's desired password."""
        return self.page.id=customer.password.or_(self.page.css=input[name='customer.password'])

    @property
    def Confirm(self):
        """Input field to confirm the user's password."""
        return self.page.id=repeatedPassword.or_(self.page.css=input[name='repeatedPassword'])

    @property
    def Register Button(self):
        """Button to submit the registration form."""
        return self.page.css=input[value='Register'].or_(self.page.xpath=//input[@value='Register'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ParaBank Registration'
        await Header text is 'Signing up is easy!'
        await Presence of all input fields (First Name, Last Name, etc.)
        await Presence of the 'Register' button