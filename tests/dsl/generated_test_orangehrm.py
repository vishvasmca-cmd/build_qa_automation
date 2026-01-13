from playwright.sync_api import Page, expect
import re

def test_orangehrm_employee_e2e(page: Page):
    page.goto('https://opensource-demo.orangehrmlive.com/')
    page.locator("[name='username']").fill('Admin')
    page.locator("[name='password']").fill('admin123')
    page.locator("button[type='submit']").click()
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList')
    page.locator("button:has-text('Add')").click()
    page.locator("[name='firstName']").fill('Resilience')
    page.locator("[name='lastName']").fill('Agent')
    page.locator("button[type='submit']").click()
    expect(page).to_have_url(re.compile('viewPersonalDetails'))