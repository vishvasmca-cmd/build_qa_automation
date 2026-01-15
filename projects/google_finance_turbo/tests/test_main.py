from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    page.goto('https://www.google.com/finance/', timeout=60000, wait_until='commit')
    page.get_by_role('link', name='Finance', exact=True).first.click()
    page.get_by_role('link', name='Finance', exact=True).first.click()
    page.locator('a[aria-label*="S&P 500"]').first.click()
    page.get_by_role('link', name='Finance', exact=True).first.click()
    page.get_by_role('combobox', name='Search for stocks, ETFs & more', exact=True).first.click()
    page.get_by_role('combobox', name='Search for stocks, ETFs & more', exact=True).first.fill('TES')