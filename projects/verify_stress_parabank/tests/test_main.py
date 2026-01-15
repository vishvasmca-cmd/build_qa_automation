from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    page.goto('https://parabank.parasoft.com/parabank/index.htm', timeout=60000, wait_until='commit')
    page.get_by_role('link', name='Site Map').first.click()
    page.get_by_role('link', name='Log Out').first.click()
    page.get_by_role('link', name='Forgot login info?', exact=True).first.click()
    page.get_by_role('link', name='Site Map').first.click()