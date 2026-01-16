from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    page.goto('https://duckduckgo.com', timeout=60000, wait_until='commit')