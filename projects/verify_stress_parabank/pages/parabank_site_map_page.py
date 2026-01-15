from playwright.async_api import Page, expect

class ParabankSiteMapPage:
    """
    The sitemap page of ParaBank provides links to various sections of the website, a customer login form, and a customer lookup form.
    URL Pattern: https://parabank.parasoft.com/parabank/sitemap.htm*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for username."""
        return self.page.id=username.or_(self.page.css=input[name='username'])

    @property
    def password_input(self):
        """Input field for password."""
        return self.page.id=password.or_(self.page.css=input[name='password'])

    @property
    def log_in_button(self):
        """Button to submit the login form."""
        return self.page.css=input[value='Log In'].or_(self.page.value=Log In)

    @property
    def forgot_login_info_(self):
        """Link to the forgot login info page."""
        return self.page.link=Forgot login info?.or_(self.page.css=a[href*='lookup'])

    @property
    def register_link(self):
        """Link to the registration page."""
        return self.page.link=Register.or_(self.page.css=a[href*='register'])

    @property
    def first_name_input(self):
        """Input field for first name in customer lookup."""
        return self.page.id=firstName.or_(self.page.css=input[name='firstName'])

    @property
    def last_name_input(self):
        """Input field for last name in customer lookup."""
        return self.page.id=lastName.or_(self.page.css=input[name='lastName'])

    @property
    def address_input(self):
        """Input field for address in customer lookup."""
        return self.page.id=address.or_(self.page.css=input[name='address'])

    @property
    def city_input(self):
        """Input field for city in customer lookup."""
        return self.page.id=city.or_(self.page.css=input[name='city'])

    @property
    def state_input(self):
        """Input field for state in customer lookup."""
        return self.page.id=state.or_(self.page.css=input[name='state'])

    @property
    def zip_code_input(self):
        """Input field for zip code in customer lookup."""
        return self.page.id=zipCode.or_(self.page.css=input[name='zipCode'])

    @property
    def ssn_input(self):
        """Input field for SSN in customer lookup."""
        return self.page.id=ssn.or_(self.page.css=input[name='ssn'])

    @property
    def find_my_login_info_button(self):
        """Button to submit the customer lookup form."""
        return self.page.css=input[value='Find My Login Info'].or_(self.page.value=Find My Login Info)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title is 'ParaBank | Site Map'
        await Page contains the header 'Customer Login'
        await Page contains the header 'Customer Lookup'
        await Page contains the text 'Please fill out the following information in order to validate your account.'