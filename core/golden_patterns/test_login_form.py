# tests/test_login.py
from playwright.sync_api import Page, expect

def test_user_can_log_in(page: Page) -> None:
    # Arrange
    page.goto("https://example.com/login")

    # Act
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Sign in").click()

    # Assert
    expect(page.get_by_text("Welcome, User")).to_be_visible()
