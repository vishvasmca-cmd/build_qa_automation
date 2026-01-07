# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        self.page.goto("https://example.com/login")

    def login(self, email: str, password: str) -> None:
        # Preferred: Label-based locators for inputs
        self.page.get_by_label("Email").fill(email)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()

    def assert_logged_in(self) -> None:
        expect(self.page.get_by_text("Welcome, User")).to_be_visible()
