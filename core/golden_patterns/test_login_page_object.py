# tests/test_login_page_object.py
from playwright.sync_api import Page
# In real usage, imports might differ, but this shows the usage pattern
from pages.login_page import LoginPage

def test_login_via_page_object(page: Page) -> None:
    login_page = LoginPage(page)

    # Arrange
    login_page.goto()

    # Act
    login_page.login("user@example.com", "password123")

    # Assert
    login_page.assert_logged_in()
