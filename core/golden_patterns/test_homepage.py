# tests/test_homepage.py
import re
from playwright.sync_api import Page, expect

def test_homepage_has_title(page: Page) -> None:
    # Arrange
    page.goto("https://example.com/")

    # Assert
    expect(page).to_have_title(re.compile("Example Domain"))
