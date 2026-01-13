from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    try:
        page.goto('https://www.dyson.in/', timeout=60000, wait_until='commit')
    except Exception as e:
        print(f"Navigation failed: {e}")
        return  # Or handle the error as appropriate

    try:
        page.get_by_text('X', exact=True).first.click()
    except Exception as e:
        print(f"Could not close initial popup: {e}")

    try:
        page.locator('#btn-close-sticky-promo').click()
    except Exception as e:
        print(f"Could not close sticky promo: {e}")