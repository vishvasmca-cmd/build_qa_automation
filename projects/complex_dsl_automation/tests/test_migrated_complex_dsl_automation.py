from playwright.sync_api import Page, expect
import re

def test_migrated_complex_dsl_automation(page: Page):
    page.goto('https://automationexercise.com/')
    page.get_by_role('link', name='Signup / Login', exact=True).first.click()
    page.locator("[name='name']").fill('Antigravity')
    page.locator("[name='email']").fill('dsl_test_complex_01@example.com')
    page.get_by_role('button', name='Signup', exact=True).first.click()
    page.get_by_text('Mr.').first.click()
    page.locator('#password').fill('password123')
    page.locator('#first_name').fill('Anti')
    page.locator('#last_name').fill('Gravity')
    page.locator('#company').fill('SpaceX')
    page.locator('#address1').fill('123 Mars Blvd')
    page.locator('#state').fill('Delhi')
    page.locator('#city').fill('New Delhi')
    page.locator('#zipcode').fill('10001')
    page.locator('#mobile_number').fill('5551234567')
    page.get_by_role('button', name='Create Account', exact=True).first.click()
    page.get_by_role('link', name='Continue', exact=True).first.click()
    page.get_by_role('link', name='Delete Account', exact=True).first.click()
    page.get_by_role('link', name='Continue', exact=True).first.click()