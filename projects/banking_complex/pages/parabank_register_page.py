from playwright.async_api import Page, expect

class ParabankRegisterPage:
    """
    Registration page for new customers of ParaBank
    URL Pattern: /register.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name_input(self):
        """Input field for the user's first name"""
        return self.page.get_by_label('First Name:').or_(self.page.locator('input[name="customer.firstName"]'))

    @property
    def last_name_input(self):
        """Input field for the user's last name"""
        return self.page.get_by_label('Last Name:').or_(self.page.locator('input[name="customer.lastName"]'))

    @property
    def address_input(self):
        """Input field for the user's address"""
        return self.page.get_by_label('Address:').or_(self.page.locator('input[name="customer.address.street"]'))

    @property
    def city_input(self):
        """Input field for the user's city"""
        return self.page.get_by_label('City:').or_(self.page.locator('input[name="customer.address.city"]'))

    @property
    def state_input(self):
        """Input field for the user's state"""
        return self.page.get_by_label('State:').or_(self.page.locator('input[name="customer.address.state"]'))

    @property
    def zip_code_input(self):
        """Input field for the user's zip code"""
        return self.page.get_by_label('Zip Code:').or_(self.page.locator('input[name="customer.address.zipCode"]'))

    @property
    def phone_input(self):
        """Input field for the user's phone number"""
        return self.page.get_by_label('Phone #:').or_(self.page.locator('input[name="customer.phoneNumber"]'))

    @property
    def ssn_input(self):
        """Input field for the user's SSN"""
        return self.page.get_by_label('SSN:').or_(self.page.locator('input[name="customer.ssn"]'))

    @property
    def username_input(self):
        """Input field for the user's desired username"""
        return self.page.get_by_label('Username:').or_(self.page.locator('input[name="customer.username"]'))

    @property
    def password_input(self):
        """Input field for the user's desired password"""
        return self.page.get_by_label('Password:').or_(self.page.locator('input[name="customer.password"]'))

    @property
    def confirm_password_input(self):
        """Input field to confirm the user's password"""
        return self.page.get_by_label('Confirm:').or_(self.page.locator('input[name="repeatedPassword"]'))

    @property
    def register_button(self):
        """Button to submit the registration form"""
        return self.page.get_by_role('button', name='Register').or_(self.page.locator('input[value="Register"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank Registration')
        await expect(page.locator('h1:has-text("Signing up is easy!")')).to_be_visible()
        await expect(page.url()).to_contain('/register.htm')