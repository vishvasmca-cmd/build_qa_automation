from playwright.sync_api import Page, expect
import re

def test_inference_test(page: Page):
    page.goto('https://example.com/login')
    page.locator("[name='username']").fill('myuser')
    page.locator("[name='password']").fill('mypass')
    page.locator("button[type='submit']").click()