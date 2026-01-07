# tests/test_api_intercept.py
import json
from playwright.sync_api import Browser, expect

def test_shows_products_from_mocked_api(browser: Browser) -> None:
    page = browser.new_page()

    # Arrange
    def handle_route(route, request):
        if "api/products" in request.url:
            body = json.dumps({"items": [{"name": "Mocked Product"}]})
            route.fulfill(status=200, content_type="application/json", body=body)
        else:
            route.continue_()

    # Pattern: Mocking logic inside the test for visibility
    page.route("**/api/**", handle_route)

    # Act
    page.goto("https://example.com/shop")

    # Assert
    expect(page.get_by_text("Mocked Product")).to_be_visible()
