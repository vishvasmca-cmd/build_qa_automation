from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page appears to be a registration or signup page for a service or application.
    URL Pattern: /register
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name_input(self):
        """Input field for the user's first name."""
        return self.page.get_by_label('First Name').or_(self.page.locator('#firstName'))

    @property
    def last_name_input(self):
        """Input field for the user's last name."""
        return self.page.get_by_label('Last Name').or_(self.page.locator('#lastName'))

    @property
    def email_input(self):
        """Input field for the user's email address."""
        return self.page.get_by_label('Email').or_(self.page.locator('#email'))

    @property
    def password_input(self):
        """Input field for the user's password."""
        return self.page.get_by_label('Password').or_(self.page.locator('#password'))

    @property
    def confirm_password_input(self):
        """Input field to confirm the user's password."""
        return self.page.get_by_label('Confirm Password').or_(self.page.locator('#confirmPassword'))

    @property
    def register_button(self):
        """Button to submit the registration form."""
        return self.page.get_by_role('button', name='Register').or_(self.page.locator('#registerButton'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('Registration')
        await expect(page.get_by_role('heading', name='Create an Account')).to_be_visible()
        await expect(page.locator('#firstName')).to_be_visible()
        await expect(page.locator('#lastName')).to_be_visible()
        await expect(page.locator('#email')).to_be_visible()
        await expect(page.locator('#password')).to_be_visible()
        await expect(page.locator('#confirmPassword')).to_be_visible()
        await expect(page.locator('#registerButton')).to_be_visible()