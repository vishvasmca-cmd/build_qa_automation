from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    try:
        page.goto('https://www.dyson.in/', timeout=60000, wait_until='commit')
    except Exception as e:
        print(f"Navigation failed: {e}")
        return
    try:
        page.get_by_text('X', exact=True).first.click()
    except:
        pass
    try:
        page.get_by_text('X', exact=True).first.click()
    except:
        pass