# tests/test_navigation.py
from playwright.sync_api import Page, expect

def test_can_navigate_to_docs(page: Page) -> None:
    # Arrange
    page.goto("https://playwright.dev/")

    # Act
    page.get_by_role("link", name="Get started").click()

    # Assert
    expect(page).to_have_url("https://playwright.dev/docs/intro")
