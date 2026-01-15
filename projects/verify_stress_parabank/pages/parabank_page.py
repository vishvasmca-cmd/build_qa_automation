from playwright.async_api import Page, expect

class ParabankPage:
    """
    The ParaBank Homepage allows users to log in, register, and access various banking services.
    URL Pattern: https://parabank.parasoft.com/parabank/index.htm*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def username_input(self):
        """Input field for username."""
        return self.page.//input[@name='username'].or_(self.page.input[name='username'])

    @property
    def password_input(self):
        """Input field for password."""
        return self.page.//input[@name='password'].or_(self.page.input[name='password'])

    @property
    def log_in_button(self):
        """Button to submit login credentials."""
        return self.page.//input[@value='Log In'].or_(self.page.input[value='Log In'])

    @property
    def forgot_login_info_(self):
        """Link to navigate to the forgot login info page."""
        return self.page.//a[contains(text(),'Forgot login info?')].or_(self.page.a:contains('Forgot login info?'))

    @property
    def register_link(self):
        """Link to navigate to the registration page."""
        return self.page.//a[contains(text(),'Register')].or_(self.page.a:contains('Register'))

    @property
    def open_new_account_link(self):
        """Link to navigate to the Open New Account page."""
        return self.page.//a[contains(text(),'Open New Account')].or_(self.page.a:contains('Open New Account'))

    @property
    def accounts_overview_link(self):
        """Link to navigate to the Accounts Overview page."""
        return self.page.//a[contains(text(),'Accounts Overview')].or_(self.page.a:contains('Accounts Overview'))

    @property
    def transfer_funds_link(self):
        """Link to navigate to the Transfer Funds page."""
        return self.page.//a[contains(text(),'Transfer Funds')].or_(self.page.a:contains('Transfer Funds'))

    @property
    def bill_pay_link(self):
        """Link to navigate to the Bill Pay page."""
        return self.page.//a[contains(text(),'Bill Pay')].or_(self.page.a:contains('Bill Pay'))

    @property
    def find_transactions_link(self):
        """Link to navigate to the Find Transactions page."""
        return self.page.//a[contains(text(),'Find Transactions')].or_(self.page.a:contains('Find Transactions'))

    @property
    def update_contact_info_link(self):
        """Link to navigate to the Update Contact Info page."""
        return self.page.//a[contains(text(),'Update Contact Info')].or_(self.page.a:contains('Update Contact Info'))

    @property
    def request_loan_link(self):
        """Link to navigate to the Request Loan page."""
        return self.page.//a[contains(text(),'Request Loan')].or_(self.page.a:contains('Request Loan'))

    @property
    def log_out_link(self):
        """Link to log out of the application."""
        return self.page.//a[contains(text(),'Log Out')].or_(self.page.a:contains('Log Out'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ParaBank | Welcome'
        await Page contains the text 'Customer Login'
        await Page contains the text 'Welcome to ParaBank'