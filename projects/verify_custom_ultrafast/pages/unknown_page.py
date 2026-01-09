from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page displays the user's financial overview, including balances, credit availability, due payments, and recent transactions.
    URL Pattern: https://demo.applitools.com/app.html
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Add Account Button(self):
        """Button to add a new account."""
        return self.page.data-test="add-account-button".or_(self.page.text=Add Account)

    @property
    def Make Payment Button(self):
        """Button to make a payment."""
        return self.page.data-test="make-payment-button".or_(self.page.text=Make Payment)

    @property
    def View Statement Link(self):
        """Link to view the account statement."""
        return self.page.text=View Statement >.or_(self.page.css=a[href*='statement'])

    @property
    def Request Increase Link(self):
        """Link to request a credit increase."""
        return self.page.text=Request Increase >.or_(self.page.css=a[href*='increase'])

    @property
    def Pay Now Link(self):
        """Link to pay the due amount."""
        return self.page.text=Pay Now >.or_(self.page.css=a[href*='pay'])

    @property
    def Credit Cards Link(self):
        """Link to navigate to credit cards page."""
        return self.page.text=Credit cards.or_(self.page.css=li[id='credit-cards'])

    @property
    def Debit Cards Link(self):
        """Link to navigate to debit cards page."""
        return self.page.text=Debit cards.or_(self.page.css=li[id='debit-cards'])

    @property
    def Loans Link(self):
        """Link to navigate to loans page."""
        return self.page.text=Loans.or_(self.page.css=li[id='loans'])

    @property
    def Mortgages Link(self):
        """Link to navigate to mortgages page."""
        return self.page.text=Mortgages.or_(self.page.css=li[id='mortgages'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'ACME Bank'
        await Header text is 'Financial Overview'
        await Total Balance is displayed
        await Credit Available is displayed
        await Due Today is displayed
        await Recent Transactions section is displayed