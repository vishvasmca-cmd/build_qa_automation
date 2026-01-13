from playwright.sync_api import Page, expect
import re

def test_generated_task(page: Page):
    page.goto('https://www.saucedemo.com/')
    page.locator("[data-test='username']").fill('standard_user')
    page.locator("[data-test='password']").fill('secret_sauce')
    page.locator("[data-test='login-button']").click()
    page.get_by_role('button', name='Add to cart', exact=True).first.click()