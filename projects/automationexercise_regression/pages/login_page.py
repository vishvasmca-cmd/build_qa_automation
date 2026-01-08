from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object for Login/Logout pages.
    Handles user authentication.
    """
    def __init__(self, page: Page):
        super().__init__(page)

    # --- Locators ---
    @property
    def email_input(self):
        """Locator for the email input field on the login form."""
        return self.page.locator("form[action='/login'] input[name='email']")

    @property
    def password_input(self):
        """Locator for the password input field on the login form."""
        return self.page.get_by_placeholder("Password")

    @property
    def login_button(self):
        """Locator for the Login button."""
        return self.page.get_by_role("button", name="Login")

    @property
    def logout_link(self):
        """Locator for the Logout link in the header."""
        return self.page.get_by_role("link", name="Logout")

    @property
    def logged_in_as_text(self):
        """Locator for the 'Logged in as...' text."""
        return self.page.get_by_text("Logged in as")

    # --- Actions ---
    def login(self, email, password):
        """Perform input and click login."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def logout(self):
        """Click the logout link."""
        self.logout_link.click()
