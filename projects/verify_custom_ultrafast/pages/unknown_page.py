from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the main dashboard page displaying the user's financial overview, including balances, credit availability, due payments, and recent transactions.
    URL Pattern: https://demo.applitools.com/app.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Add Account Button(self):
        """Button to add a new account."""
        return self.page.Add Account.or_(self.page.css=.btn.btn-primary.add-account)

    @property
    def Make Payment Button(self):
        """Button to make a payment."""
        return self.page.Make Payment.or_(self.page.css=.btn.btn-success.make-payment)

    @property
    def View Statement Link(self):
        """Link to view the account statement."""
        return self.page.View Statement.or_(self.page.css=a[href='/statement'])

    @property
    def Request Increase Link(self):
        """Link to request a credit limit increase."""
        return self.page.Request Increase.or_(self.page.css=a[href='/increase'])

    @property
    def Pay Now Link(self):
        """Link to pay the due amount."""
        return self.page.Pay Now.or_(self.page.css=a[href='/pay'])

    @property
    def Credit Cards Menu Item(self):
        """Menu item to navigate to credit cards section."""
        return self.page.Credit cards.or_(self.page.css=#creditCards)

    @property
    def Debit Cards Menu Item(self):
        """Menu item to navigate to debit cards section."""
        return self.page.Debit cards.or_(self.page.css=#debitCards)

    @property
    def Loans Menu Item(self):
        """Menu item to navigate to loans section."""
        return self.page.Loans.or_(self.page.css=#loans)

    @property
    def Mortgages Menu Item(self):
        """Menu item to navigate to mortgages section."""
        return self.page.Mortgages.or_(self.page.css=#mortgages)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ACME demo app'
        await Header 'Financial Overview' is displayed
        await Total Balance is displayed
        await Credit Available is displayed
        await Due Today is displayed
        await Recent Transactions section is displayed