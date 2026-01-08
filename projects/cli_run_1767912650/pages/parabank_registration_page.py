from playwright.async_api import Page, expect

class ParabankRegistrationPage:
    """
    Registration page for new customers
    URL Pattern: /register.htm
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def firstName(self):
        """First Name input field"""
        return self.page.get_by_label('First Name:').or_(self.page.locator('[name="customer.firstName"]'))

    @property
    def lastName(self):
        """Last Name input field"""
        return self.page.get_by_label('Last Name:').or_(self.page.locator('[name="customer.lastName"]'))

    @property
    def address(self):
        """Address input field"""
        return self.page.get_by_label('Address:').or_(self.page.locator('[name="customer.address.street"]'))

    @property
    def city(self):
        """City input field"""
        return self.page.get_by_label('City:').or_(self.page.locator('[name="customer.address.city"]'))

    @property
    def state(self):
        """State input field"""
        return self.page.get_by_label('State:').or_(self.page.locator('[name="customer.address.state"]'))

    @property
    def zipCode(self):
        """Zip Code input field"""
        return self.page.get_by_label('Zip Code:').or_(self.page.locator('[name="customer.address.zipCode"]'))

    @property
    def phone(self):
        """Phone Number input field"""
        return self.page.get_by_label('Phone #:').or_(self.page.locator('[name="customer.phoneNumber"]'))

    @property
    def ssn(self):
        """SSN input field"""
        return self.page.get_by_label('SSN:').or_(self.page.locator('[name="customer.ssn"]'))

    @property
    def username(self):
        """Username input field"""
        return self.page.get_by_label('Username:').or_(self.page.locator('[name="customer.username"]'))

    @property
    def password(self):
        """Password input field"""
        return self.page.get_by_label('Password:').or_(self.page.locator('[name="customer.password"]'))

    @property
    def confirm(self):
        """Confirm Password input field"""
        return self.page.get_by_label('Confirm:').or_(self.page.locator('[name="repeatedPassword"]'))

    @property
    def register_btn(self):
        """Register button"""
        return self.page.get_by_role('button', name='Register').or_(self.page.locator('input[value="Register"]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ParaBank Registration')
        await expect(page.locator('text=Signing up is easy!')).to_be_visible()