from playwright.async_api import Page, expect

class HomePage:
    """
    The Home Page of the Automation Exercise website serves as the landing page, providing an overview of the site's purpose and key features. It aims to attract QA engineers looking for automation practice and API testing resources.
    URL Pattern: https://www.automationexercise.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Home Link(self):
        """Link to navigate back to the home page."""
        return self.page.role=link[name="Home"].or_(self.page.text=Home)

    @property
    def Products Link(self):
        """Link to navigate to the products page."""
        return self.page.role=link[name="Products"].or_(self.page.text=Products)

    @property
    def Cart Link(self):
        """Link to navigate to the shopping cart page."""
        return self.page.role=link[name="Cart"].or_(self.page.text=Cart)

    @property
    def Signup / Login Link(self):
        """Link to navigate to the signup or login page."""
        return self.page.role=link[name="Signup / Login"].or_(self.page.text=Signup / Login)

    @property
    def Test Cases Link(self):
        """Link to navigate to the test cases page."""
        return self.page.role=link[name="Test Cases"].or_(self.page.text=Test Cases)

    @property
    def API Testing Link(self):
        """Link to navigate to the API testing page."""
        return self.page.role=link[name="API Testing"].or_(self.page.text=API Testing)

    @property
    def Contact Us Link(self):
        """Link to navigate to the contact us page."""
        return self.page.role=link[name="Contact us"].or_(self.page.text=Contact us)

    @property
    def Test Cases Button(self):
        """Button to navigate to the test cases page."""
        return self.page.role=button[name="Test Cases"].or_(self.page.text=Test Cases)

    @property
    def APIs list for practice Button(self):
        """Button to navigate to the APIs list page."""
        return self.page.role=button[name="APIs list for practice"].or_(self.page.text=APIs list for practice)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'Automation Exercise'
        await Header text contains 'AutomationExercise'
        await The main description includes 'Full-Fledged practice website for Automation Engineers'