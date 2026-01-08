from playwright.async_api import Page, expect

class ParabankRegisterPage:
    """
    Registration page for new customer accounts
    URL Pattern: /register
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name(self):
        """Input field for the first name of the user"""
        return self.page.get_by_label('First Name:').or_(self.page.locator('input[name="customer.firstName"]'))

    @property
    def last_name(self):
        """Input field for the last name of the user"""
        return self.page.get_by_label('Last Name:').or_(self.page.locator('input[name="customer.lastName"]'))

    @property
    def address(self):
        """Input field for the address of the user"""
        return self.page.get_by_label('Address:').or_(self.page.locator('input[name="customer.address.street"]'))

    @property
    def city(self):
        """Input field for the city of the user"""
        return self.page.get_by_label('City:').or_(self.page.locator('input[name="customer.address.city"]'))

    @property
    def state(self):
        """Input field for the state of the user"""
        return self.page.get_by_label('State:').or_(self.page.locator('input[name="customer.address.state"]'))

    @property
    def zip_code(self):
        """Input field for the zip code of the user"""
        return self.page.get_by_label('Zip Code:').or_(self.page.locator('input[name="customer.address.zipCode"]'))

    @property
    def phone(self):
        """Input field for the phone number of the user"""
        return self.page.get_by_label('Phone #:').or_(self.page.locator('input[name="customer.phoneNumber"]'))

    @property
    def ssn(self):
        """Input field for the ssn of the user"""
        return self.page.get_by_label('SSN:').or_(self.page.locator('input[name="customer.ssn"]'))

    @property
    def username(self):
        """Input field for the username of the user"""
        return self.page.get_by_label('Username:').or_(self.page.locator('input[name="customer.username"]'))

    @property
    def password(self):
        """Input field for the password of the user"""
        return self.page.get_by_label('Password:').or_(self.page.locator('input[name="customer.password"]'))

    @property
    def confirm(self):
        """Input field to confirm the password of the user"""
        return self.page.get_by_label('Confirm:').or_(self.page.locator('input[name="repeatedPassword"]'))

    @property
    def register_btn(self):
        """Submission button for registration"""
        return self.page.get_by_role('button', name='Register').or_(self.page.locator('input[value="Register"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank Registration')
        await expect(page.get_by_text('Signing up is easy!')).to_be_visible()