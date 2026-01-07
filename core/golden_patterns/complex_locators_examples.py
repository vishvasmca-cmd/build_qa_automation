# golden/complex_locators_examples.py
from playwright.sync_api import Page, expect

def test_dynamic_product_cards(page: Page) -> None:
    # Goal: Click "Add to cart" for "Product 2" in a list of cards
    page.goto("https://example.com/products")
    product = page.get_by_test_id("product-card").filter(has_text="Product 2")
    product.get_by_role("button", name="Add to cart").click()


def test_complex_filter_panel(page: Page) -> None:
    # Goal: Fill "Min" in the Rating group (avoiding "Min" in Price group)
    page.goto("https://example.com/filters")
    rating_group = page.get_by_test_id("filter-group").filter(has_text="Rating")
    rating_group.get_by_label("Min").fill("4")


def test_optional_modal_or_main(page: Page) -> None:
    # Goal: Handle optional security dialog if it appears
    page.goto("https://example.com/app")
    new_email = page.get_by_test_id("new-email")
    security_dialog = page.get_by_test_id("security-dialog")

    # Use .or_() to wait for either
    winner = security_dialog.or_(new_email)
    winner.wait_for()

    if security_dialog.is_visible():
        page.get_by_test_id("confirm-device").click()
    else:
        new_email.click()


def test_nested_shadow_dom(page: Page) -> None:
    # Goal: Open menu for a user card (Shadow DOM pierced automatically)
    page.goto("https://example.com/users")
    user = page.get_by_test_id("user-card").filter(has_text="Alice Johnson")
    user.get_by_role("button", name="Open menu").click()


def test_table_multi_column_match(page: Page) -> None:
    # Goal: Click "Pay now" for order A123 that is Pending with total $25.00
    page.goto("https://example.com/orders")
    row = page.get_by_test_id("order-row").filter(
        has_text="A123",
    ).filter(
        has_text="Pending",
    ).filter(
        has_text="$25.00",
    )
    row.get_by_role("button", name="Pay now").click()


def test_tabbed_ui_semantic(page: Page) -> None:
    # Goal: Switch to "Security" tab and verify the panel
    page.goto("https://example.com/settings")
    page.get_by_role("tab", name="Security").click()
    security_panel = page.get_by_role("tabpanel", name="Security")
    expect(security_panel.get_by_text("Security")).to_be_visible()


def test_composite_search_result(page: Page) -> None:
    # Goal: Click "Open" on result with title "Locator" and tag "Guide"
    page.goto("https://example.com/search")
    result = page.get_by_test_id("search-result").filter(
        has_text="Locator",
    ).filter(
        has_text="Guide",
    )
    result.get_by_role("button", name="Open").click()
