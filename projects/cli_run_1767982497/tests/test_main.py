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

    def navigate_to_login_page(self):
        self.navigate(self.url)

    def enter_username(self, username):
        self.page.locator("[name='username']").fill(username)

    def enter_password(self, password):
        self.page.locator("[name='password']").fill(password)

    def click_login_button(self):
        self.page.locator("input[value='Log In']").click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def click_register_link(self):
        self.page.get_by_role("link", name="Register").click()

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/register.htm"

    def navigate_to_registration_page(self):
        self.navigate(self.url)

    def fill_registration_form(
        self,
        first_name,
        last_name,
        address,
        city,
        state,
        zip_code,
        phone,
        ssn,
        username,
        password,
        confirm_password,
    ):
        self.page.locator("[id='customer.firstName']").fill(first_name)
        self.page.locator("[id='customer.lastName']").fill(last_name)
        self.page.locator("[id='customer.address.street']").fill(address)
        self.page.locator("[id='customer.address.city']").fill(city)
        self.page.locator("[id='customer.address.state']").fill(state)
        self.page.locator("[id='customer.address.zipCode']").fill(zip_code)
        self.page.locator("[id='customer.phoneNumber']").fill(phone)
        self.page.locator("[id='customer.ssn']").fill(ssn)
        self.page.locator("[id='customer.username']").fill(username)
        self.page.locator("[id='customer.password']").fill(password)
        self.page.locator("[id='repeatedPassword']").fill(confirm_password)

    def click_register_button(self):
        self.page.locator("input[value='Register']").click()

class AccountServicesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def open_new_account(self):
        self.page.get_by_role("link", name="Open New Account").click()

    def select_account_type(self, account_type):
        self.page.get_by_label("Type of Account:").select_option(label=account_type)

    def click_open_new_account_button(self):
        self.page.locator("input[value='Open New Account']").click()

    def transfer_funds(self, from_account, to_account, amount):
        self.page.get_by_role("link", name="Transfer Funds").click()
        self.page.locator("[id='amount']").fill(amount)
        self.page.locator("[id='fromAccountId']").select_option(label=from_account)
        self.page.locator("[id='toAccountId']").select_option(label=to_account)
        self.page.locator("input[value='Transfer']").click()

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def login(self, username, password):
        self.page.locator("[name='username']").fill(username)
        self.page.locator("[name='password']").fill(password)
        self.page.locator("input[value='Log In']").click()

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    registration_page = RegistrationPage(page)
    account_services_page = AccountServicesPage(page)
    home_page = HomePage(page)

    # Register a new user
    login_page.navigate_to_login_page()
    login_page.click_register_link()
    registration_page.fill_registration_form(
        first_name="John",
        last_name="Doe",
        address="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="12345",
        phone="555-555-5555",
        ssn="123-45-6789",
        username="john.doe123",
        password="password",
        confirm_password="password",
    )
    registration_page.click_register_button()

    # Login
    home_page.login(username="john.doe123", password="password")

    # Open New Savings Account
    account_services_page.open_new_account()
    account_services_page.select_account_type(account_type="Savings")
    account_services_page.click_open_new_account_button()

    # Find the account ID of the newly created account
    new_account_id = page.locator("#newAccountId").inner_text()

    # Open another account to transfer funds between
    account_services_page.open_new_account()
    account_services_page.select_account_type(account_type="Checking")
    account_services_page.click_open_new_account_button()

    # Find the account ID of the second created account
    second_account_id = page.locator("#newAccountId").inner_text()

    # Transfer Funds
    account_services_page.transfer_funds(
        from_account=new_account_id,
        to_account=second_account_id,
        amount="100"
    )