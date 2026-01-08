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

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/index.htm"

    def navigate(self):
        super().navigate(self.url)

    def click_register_link(self):
        self.page.get_by_role("link", name="Register").click()

class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/register.htm"

    def navigate(self):
        super().navigate(self.url)

    def fill_first_name(self, first_name):
        # The traceback shows that the locator uses an invalid escape sequence. Fixing it.
        self.page.locator("#customer\\.firstName").fill(first_name)

    def fill_last_name(self, last_name):
        self.page.locator("#customer\\.lastName").fill(last_name)

    def fill_address(self, address):
        self.page.locator("#customer\\.address\\.street").fill(address)

    def fill_city(self, city):
        self.page.locator("#customer\\.address\\.city").fill(city)

    def fill_state(self, state):
        self.page.locator("#customer\\.address\\.state").fill(state)

    def fill_zip_code(self, zip_code):
        self.page.locator("#customer\\.address\\.zipCode").fill(zip_code)

    def fill_phone_number(self, phone_number):
        self.page.locator("#customer\\.phoneNumber").fill(phone_number)

    def fill_ssn(self, ssn):
        self.page.locator("#customer\\.ssn").fill(ssn)

    def fill_username(self, username):
        self.page.locator("#customer\\.username").fill(username)

    def fill_password(self, password):
        self.page.locator("#customer\\.password").fill(password)

    def fill_confirm_password(self, confirm_password):
        self.page.locator("#customer\\.repeatedPassword").fill(confirm_password)

    def click_register_button(self):
        self.page.locator("input[value='Register']").click()

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/login.htm"

    def navigate(self):
        super().navigate(self.url)

    def fill_username(self, username):
        self.page.locator("input[name='username']").fill(username)

    def fill_password(self, password):
        self.page.locator("input[name='password']").fill(password)

    def click_login_button(self):
        self.page.locator("input[value='Log In']").click()

class AccountServicesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/account.htm"

    def navigate(self):
        super().navigate(self.url)

    def click_open_new_account_link(self):
        self.page.get_by_role("link", name="Open New Account").click()

    def click_transfer_funds_link(self):
        self.page.get_by_role("link", name="Transfer Funds").click()

    def click_request_loan_link(self):
        self.page.get_by_role("link", name="Request Loan").click()

class OpenAccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/openaccount.htm"

    def navigate(self):
        super().navigate(self.url)

    def select_account_type(self, account_type):
        self.page.locator("#type").select_option(label=account_type)

    def click_open_new_account_button(self):
        self.page.locator("input[value='Open New Account']").click()

class TransferFundsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/transfer.htm"

    def navigate(self):
        super().navigate(self.url)

    def fill_amount(self, amount):
        self.page.locator("#amount").fill(amount)

    def select_from_account(self, account_id):
         self.page.locator("#fromAccountId").select_option(label=account_id)

    def select_to_account(self, account_id):
        self.page.locator("#toAccountId").select_option(label=account_id)

    def click_transfer_button(self):
        self.page.locator("input[value='Transfer']").click()

class RequestLoanPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://parabank.parasoft.com/parabank/requestloan.htm"

    def navigate(self):
        super().navigate(self.url)

    def fill_loan_amount(self, amount):
        self.page.locator("#amount").fill(amount)

    def fill_down_payment(self, amount):
        self.page.locator("#downPayment").fill(amount)

    def select_from_account(self, account_id):
        self.page.locator("#fromAccountId").select_option(label=account_id)

    def click_apply_now_button(self):
        self.page.locator("input[value='Apply Now']").click()

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    home_page = HomePage(page)
    register_page = RegisterPage(page)
    account_services_page = AccountServicesPage(page)
    open_account_page = OpenAccountPage(page)
    transfer_funds_page = TransferFundsPage(page)
    request_loan_page = RequestLoanPage(page)
    login_page = LoginPage(page)

    # Register
    home_page.navigate()
    home_page.click_register_link()

    register_page.fill_first_name("John")
    register_page.fill_last_name("Doe")
    register_page.fill_address("123 Main St")
    register_page.fill_city("Anytown")
    register_page.fill_state("CA")
    register_page.fill_zip_code("12345")
    register_page.fill_phone_number("555-555-5555")
    register_page.fill_ssn("123-45-6789")
    register_page.fill_username("testuser")
    register_page.fill_password("password")
    register_page.fill_confirm_password("password")
    register_page.click_register_button()

    # Login
    login_page.navigate()
    login_page.fill_username("testuser")
    login_page.fill_password("password")
    login_page.click_login_button()

    # Open Account
    account_services_page.click_open_new_account_link()
    open_account_page.select_account_type("CHECKING") # or SAVINGS. CHECKING is default.
    open_account_page.click_open_new_account_button()
    page.wait_for_load_state("networkidle")

    # Get new account ID.  This is not covered in the trace, but is needed for the other steps
    new_account_id = page.locator("#newAccountId").inner_text()

    # Transfer Funds
    account_services_page.click_transfer_funds_link()
    transfer_funds_page.fill_amount("100")
    transfer_funds_page.select_from_account(new_account_id)
    transfer_funds_page.select_to_account("12345") # Example account, you would need valid account
    transfer_funds_page.click_transfer_button()

    # Request Loan
    account_services_page.click_request_loan_link()
    request_loan_page.fill_loan_amount("1000")
    request_loan_page.fill_down_payment("100")
    request_loan_page.select_from_account(new_account_id)
    request_loan_page.click_apply_now_button()
