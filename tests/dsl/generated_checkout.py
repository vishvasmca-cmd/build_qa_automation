from playwright.sync_api import Page, expect
import re

def test_saucedemo_checkout(page: Page):
    page.goto('https://www.saucedemo.com/')
    page.locator("[id='user-name']").fill('standard_user')
    page.locator("[id='password']").fill('secret_sauce')
    page.locator("[id='login-button']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator('.shopping_cart_link').click()
    page.locator("[data-test='checkout']").click()
    page.locator("[data-test='firstName']").fill('John')
    page.locator("[data-test='lastName']").fill('Doe')
    page.locator("[data-test='postalCode']").fill('12345')
    page.locator("[data-test='continue']").click()
    page.locator("[data-test='finish']").click()
    expect(page.locator('body')).to_contain_text('Thank you for your order')