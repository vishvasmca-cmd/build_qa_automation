from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    page.goto('https://www.dyson.in/', timeout=60000)
    page.get_by_text('X', exact=True).first.click()