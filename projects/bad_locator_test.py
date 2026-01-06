import re
from playwright.sync_api import Page, expect

def test_fixed_locators(page: Page):
    page.goto("https://magento.softwaretestingboard.com/")
    # Replaced brittle CSS with get_by_role
    page.get_by_role("button", name=re.compile("Shop New Yoga", re.IGNORECASE)).first().click()
    page.get_by_role("button", name=re.compile("Submit", re.IGNORECASE)).click()
    expect(page).to_have_url(re.compile(".*/yoga-equipment.html"))
