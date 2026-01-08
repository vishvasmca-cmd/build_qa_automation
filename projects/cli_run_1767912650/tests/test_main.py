# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/lib/templates')
from helpers import take_screenshot


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/index.htm"

    def navigate_to_registration(self):
        self.page.get_by_role("link", name="Register").click()

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def fill_registration_form(
        self,
        first_name,
        last_name,
        address,
        city,
        state,
        zip_code,
        phone_number,
        ssn,
        username,
        password,
        confirm_password,
    ):
        self.page.locator("[name='customer.firstName']").fill(first_name)
        self.page.locator("[name='customer.lastName']").fill(last_name)
        self.page.locator("[name='customer.address.street']").fill(address)
        self.page.locator("[name='customer.address.city']").fill(city)
        self.page.locator("[name='customer.address.state']").fill(state)
        self.page.locator("[name='customer.address.zipCode']").fill(zip_code)
        self.page.locator("[name='customer.phoneNumber']").fill(phone_number)
        self.page.locator("[name='customer.ssn']").fill(ssn)
        self.page.locator("[name='customer.username']").fill(username)
        self.page.locator("[name='customer.password']").fill(password)
        self.page.locator("[name='repeatedPassword']").fill(confirm_password)

    def register(self):
        self.page.get_by_role("button", name="Register").click()
        self.page.wait_for_load_state("networkidle")

from playwright.sync_api import Browser, expect

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()

    login_page = LoginPage(page)
    registration_page = RegistrationPage(page)

    login_page.navigate(login_page.url)
    expect(page).to_have_url(login_page.url)

    # Register
    login_page.navigate_to_registration()
    registration_page.fill_registration_form(
        first_name="John",
        last_name="Doe",
        address="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="12345",
        phone_number="123-456-7890",
        ssn="123-45-678",
        username="test",
        password="test",
        confirm_password="test",
    )

    registration_page.register()