
import pytest
import time
import re
from playwright.sync_api import Page, Browser, expect

# --- Page Objects (Inline to avoid Import Errors) ---

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

class HomePage(BasePage):
    def navigate(self):
        super().navigate("https://parabank.parasoft.com/parabank/index.htm")

    def click_register_link(self):
        self.page.get_by_role("link", name="Register").click()

class RegisterPage(BasePage):
    def fill_registration_form(self, username):
        self.page.locator("[id='customer.firstName']").fill("John")
        self.page.locator("[id='customer.lastName']").fill("Doe")
        self.page.locator("[id='customer.address.street']").fill("123 Main St")
        self.page.locator("[id='customer.address.city']").fill("New York")
        self.page.locator("[id='customer.address.state']").fill("NY")
        self.page.locator("[id='customer.address.zipCode']").fill("10001")
        self.page.locator("[id='customer.phoneNumber']").fill("555-1234")
        self.page.locator("[id='customer.ssn']").fill("123-456-7890")
        
        self.page.locator("[id='customer.username']").fill(username)
        self.page.locator("[id='customer.password']").fill("password")
        self.page.locator("[id='repeatedPassword']").fill("password")

    def click_register_button(self):
        self.page.get_by_role("button", name="Register").click()

class AccountServicesPage(BasePage):
    def click_open_new_account_link(self):
        self.page.get_by_role("link", name="Open New Account").click()

    def click_transfer_funds_link(self):
        self.page.get_by_role("link", name="Transfer Funds").click()
    
    def click_request_loan_link(self):
        self.page.get_by_role("link", name="Request Loan").click()

class OpenNewAccountPage(BasePage):
    def select_account_type(self, account_type):
        self.page.locator("#type").select_option(label=account_type)

    def click_open_new_account_button(self):
        # Use a more robust selector if "Open New Account" text appears multiple times
        self.page.locator("input.button[value='Open New Account']").click()

    def get_new_account_id(self):
        # Wait for the result to appear
        self.page.wait_for_selector("#newAccountId")
        return self.page.locator("#newAccountId").inner_text()

class TransferFundsPage(BasePage):
    def fill_transfer_form(self, amount, from_account):
        self.page.locator("#amount").fill(amount)
        # Select 'from' account - wait for options to be populated
        self.page.locator("#fromAccountId").click() # trigger validation/load
        self.page.locator("#fromAccountId").select_option(label=from_account)
        # 'to' account can be the same or dynamic. For verified workflow we pick the first available or hardcode valid if known.
        # Here we just select the first index for simplicity or a known existing one? 
        # Actually Parabank default account is usually 12345 or similar.
        # Let's select the first option index 0 for toAccount
        self.page.locator("#toAccountId").select_option(index=0) 

    def click_transfer_button(self):
        self.page.locator("input.button[value='Transfer']").click()

class RequestLoanPage(BasePage):
    def fill_loan_form(self, amount, down_payment, from_account):
        self.page.locator("#amount").fill(amount)
        self.page.locator("#downPayment").fill(down_payment)
        self.page.locator("#fromAccountId").select_option(label=from_account)

    def click_apply_now_button(self):
        self.page.locator("input.button[value='Apply Now']").click()


# --- Main Test ---

def test_autonomous_banking_flow(page: Page):
    # Setup Page Objects
    home_page = HomePage(page)
    register_page = RegisterPage(page)
    account_services = AccountServicesPage(page)
    open_account_page = OpenNewAccountPage(page)
    transfer_page = TransferFundsPage(page)
    loan_page = RequestLoanPage(page)

    # 1. Registration
    print("Step 1: Registration")
    home_page.navigate()
    home_page.click_register_link()
    
    # Generate random user
    username = f"user_{int(time.time())}"
    print(f"Registering user: {username}")
    
    register_page.fill_registration_form(username)
    register_page.click_register_button()
    
    # Verification of Registration Success (and implicit Auto-Login)
    expect(page.get_by_text(f"Welcome {username}")).to_be_visible(timeout=10000)
    print("Registration successful & Auto-logged in.")

    # 2. Login (SKIPPED - Auto-login active)
    # login_page.login(username, "password")

    # 3. Open New Account
    print("Step 3: Open New Account")
    account_services.click_open_new_account_link()
    open_account_page.select_account_type("CHECKING")
    # Wait for the button to be stable
    page.wait_for_timeout(1000) 
    open_account_page.click_open_new_account_button()
    
    new_account_id = open_account_page.get_new_account_id()
    print(f"New Account Opened: {new_account_id}")

    # 4. Transfer Funds
    print("Step 4: Transfer Funds")
    account_services.click_transfer_funds_link()
    # Wait for page to load potentially slow dropdowns
    page.wait_for_load_state("networkidle")
    transfer_page.fill_transfer_form("100", new_account_id)
    transfer_page.click_transfer_button()
    
    # Verify Transfer Complete
    expect(page.get_by_text("Transfer Complete!")).to_be_visible(timeout=10000)
    print("Transfer Complete.")

    # 5. Request Loan
    print("Step 5: Request Loan")
    account_services.click_request_loan_link()
    loan_page.fill_loan_form("1000", "100", new_account_id)
    loan_page.click_apply_now_button()
    
    # Verify Loan Processed
    expect(page.get_by_text("Loan Request Processed")).to_be_visible(timeout=10000)
    print("Loan Request Processed.")

