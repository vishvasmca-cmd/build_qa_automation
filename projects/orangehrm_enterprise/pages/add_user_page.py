from playwright.async_api import Page, expect

class AddUserPage:
    """
    This page is used to add a new user to the OrangeHRM system.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def User Role Dropdown(self):
        """Dropdown to select the user role (Admin or ESS)."""
        return self.page.User Role*.or_(self.page.div:nth-child(1) > div.oxd-input-group.oxd-input-field-bottom-space > div > div:nth-child(2) > div > div > div.oxd-select-text.oxd-select-text--active)

    @property
    def Employee Name Input(self):
        """Input field to enter the employee's name."""
        return self.page.Employee Name*.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Username Input(self):
        """Input field to enter the username."""
        return self.page.Username*.or_(self.page.div:nth-child(3) > div.oxd-input-group.oxd-input-field-bottom-space > div > div:nth-child(2) > input)

    @property
    def Password Input(self):
        """Input field to enter the password."""
        return self.page.Password*.or_(self.page.div:nth-child(1) > div.oxd-input-group.oxd-input-field-bottom-space > div > div:nth-child(2) > input)

    @property
    def Confirm Password Input(self):
        """Input field to confirm the password."""
        return self.page.Confirm Password*.or_(self.page.div:nth-child(2) > div.oxd-input-group.oxd-input-field-bottom-space > div > div:nth-child(2) > input)

    @property
    def Cancel Button(self):
        """Button to cancel adding a new user."""
        return self.page.//button[text()=' Cancel '].or_(self.page.button.oxd-button.oxd-button--secondary.orangehrm-left-space)

    @property
    def Save Button(self):
        """Button to save the new user."""
        return self.page.//button[text()=' Save '].or_(self.page.button.oxd-button.oxd-button--medium.oxd-button--secondary.orangehrm-left-space)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'OrangeHRM'
        await Header text is 'Add User'
        await URL contains '/admin/saveSystemUser'