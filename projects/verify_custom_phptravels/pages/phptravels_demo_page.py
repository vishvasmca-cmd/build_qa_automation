from playwright.async_api import Page, expect

class PhptravelsDemoPage:
    """
    This is the demo page for PHPTravels, showcasing their travel booking software and allowing users to request an instant demo.
    URL Pattern: https://phptravels.com/demo
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def First Name Input(self):
        """Input field for the user's first name."""
        return self.page.input[name='first_name'].or_(self.page.input[placeholder='Enter first name'])

    @property
    def Last Name Input(self):
        """Input field for the user's last name."""
        return self.page.input[name='last_name'].or_(self.page.input[placeholder='Enter last name'])

    @property
    def Business Name Input(self):
        """Input field for the user's business name."""
        return self.page.input[name='business_name'].or_(self.page.input[placeholder='Enter business name'])

    @property
    def WhatsApp Number Input(self):
        """Input field for the user's WhatsApp number."""
        return self.page.input[name='phone'].or_(self.page.input[placeholder='Enter WhatsApp number'])

    @property
    def Country Select(self):
        """Dropdown for selecting the user's country."""
        return self.page.select[name='country'].or_(self.page.div[class='select2-container'])

    @property
    def "Get Started" Button(self):
        """Button to navigate to the registration page."""
        return self.page.a:has-text('Get Started').or_(self.page.a[class*='btn-primary'])

    @property
    def "Login" Button(self):
        """Button to navigate to the login page."""
        return self.page.a:has-text('Login').or_(self.page.a[class*='btn-secondary'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'PHPTRAVELS Demo'
        await Header text contains 'Demo Travel Software'
        await Form with label 'Request Instant Demo' is visible