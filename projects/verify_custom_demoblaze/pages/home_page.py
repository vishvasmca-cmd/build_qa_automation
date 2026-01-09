from playwright.async_api import Page, expect

class HomePage:
    """
    The home page of the Demoblaze e-commerce website, displaying product categories, featured products, and navigation links. The screenshot also shows the 'Sign up' modal.
    URL Pattern: https://www.demoblaze.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Input(self):
        """Input field for username during sign-up."""
        return self.page.//input[@id='sign-username'].or_(self.page.css=#sign-username)

    @property
    def Password Input(self):
        """Input field for password during sign-up."""
        return self.page.//input[@id='sign-password'].or_(self.page.css=#sign-password)

    @property
    def Sign up Button(self):
        """Button to submit the sign-up form."""
        return self.page.//button[text()='Sign up'].or_(self.page.css=.btn.btn-primary)

    @property
    def Close Button(self):
        """Button to close the sign-up modal."""
        return self.page.//button[text()='Close'].or_(self.page.css=.btn.btn-secondary)

    @property
    def Phones Category(self):
        """Link to navigate to the 'Phones' category."""
        return self.page.//a[text()='Phones'].or_(self.page.css=#itemc)

    @property
    def Laptops Category(self):
        """Link to navigate to the 'Laptops' category."""
        return self.page.//a[text()='Laptops'].or_(self.page.//a[contains(text(),'Laptops')])

    @property
    def Monitors Category(self):
        """Link to navigate to the 'Monitors' category."""
        return self.page.//a[text()='Monitors'].or_(self.page.//a[contains(text(),'Monitors')])

    @property
    def Sign up Link(self):
        """Link to open the sign-up modal."""
        return self.page.//a[text()='Sign up'].or_(self.page.css=#signin2)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'STORE'
        await Presence of 'Categories' section
        await Presence of featured products (e.g., Samsung galaxy s6, Nokia lumia 1520, Nexus 6)
        await Sign up modal is visible