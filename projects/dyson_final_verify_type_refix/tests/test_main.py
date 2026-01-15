from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    page.goto('https://www.dyson.in/', timeout=60000, wait_until='commit')
    page.locator("[data-agent-id='33']").click()
    page.get_by_role('button', name='Search products and parts', exact=True).first.click()
    page.locator("[name='q']").fill('Dyson V15 Detect')
    page.get_by_label('Search products and parts').click()
    page.get_by_label('Close').click()
    page.get_by_role('link', name='Latest technology Dyson WashG1™ (Ultra Blue/Matt Black) wet ').first.click()