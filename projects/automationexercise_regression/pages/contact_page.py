from playwright.sync_api import Page
from .base_page import BasePage

class ContactPage(BasePage):
    """
    Page Object for the Contact Us page.
    Handles form filling and submission.
    """
    def __init__(self, page: Page):
        super().__init__(page)

    # --- Locators ---
    @property
    def name_input(self):
        return self.page.get_by_placeholder("Name")

    @property
    def email_input(self):
        return self.page.get_by_placeholder("Email", exact=True)

    @property
    def subject_input(self):
        return self.page.get_by_placeholder("Subject")

    @property
    def message_input(self):
        return self.page.get_by_placeholder("Your Message Here")

    @property
    def upload_file_input(self):
        return self.page.locator("input[name='upload_file']")

    @property
    def submit_button(self):
        return self.page.get_by_role("button", name="Submit")

    # --- Actions ---
    def fill_contact_form(self, name: str, email: str, subject: str, message: str):
        """Fill out the contact form fields."""
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.subject_input.fill(subject)
        self.message_input.fill(message)

    def submit_form(self):
        """
        Submit the form and handle the native browser alert that appears.
        (Note: automationexercise.com uses a window.confirm() on submit)
        """
        self.page.on("dialog", lambda dialog: dialog.accept()) # Handle JS Alert
        self.submit_button.click()
