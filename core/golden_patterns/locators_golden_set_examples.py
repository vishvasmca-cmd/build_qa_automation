# golden/locators_golden_set_examples.py
from playwright.sync_api import Page, expect

def test_button_with_aria_name(page: Page) -> None:
    page.goto("https://example.com/button-page")
    save_button = page.get_by_role("button", name="Save changes")
    save_button.click()
    expect(page.get_by_text("Saved")).to_be_visible()


def test_labeled_email_input(page: Page) -> None:
    page.goto("https://example.com/login")
    page.get_by_label("Email address").fill("user@example.com")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_text("Welcome, User")).to_be_visible()


def test_user_card_with_testid(page: Page) -> None:
    page.goto("https://example.com/users")
    user_card = page.get_by_test_id("user-card").filter(has_text="Alice Johnson")
    expect(user_card.get_by_text("Admin")).to_be_visible()


def test_listitem_navigation(page: Page) -> None:
    page.goto("https://example.com/dashboard")
    page.get_by_role("listitem", name="Settings").click()
    expect(page).to_have_url("https://example.com/settings")


def test_order_row_details_button(page: Page) -> None:
    page.goto("https://example.com/orders")
    row = page.get_by_test_id("order-row").filter(has_text="A123")
    row.get_by_role("button", name="Details").click()
    expect(page.get_by_text("Order A123 details")).to_be_visible()


def test_nav_link_with_aria_label(page: Page) -> None:
    page.goto("https://example.com")
    page.get_by_role("link", name="Account settings").click()
    expect(page).to_have_url("https://example.com/settings")


def test_checkbox_with_label(page: Page) -> None:
    page.goto("https://example.com/terms")
    checkbox = page.get_by_label("I agree to the Terms and Conditions")
    checkbox.check()
    expect(checkbox).to_be_checked()
