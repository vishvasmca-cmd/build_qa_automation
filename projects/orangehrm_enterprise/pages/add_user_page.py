from playwright.async_api import Page, expect

class AddUserPage:
    """
    This page is used to add a new user to the OrangeHRM system.
    URL Pattern: /web/index.php/admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def User Role Dropdown(self):
        """Dropdown to select the user role (Admin or ESS)."""
        return self.page.User Role*.or_(self.page.div:nth-child(1) > div:nth-child(1) > div > div:nth-child(2) > i)

    @property
    def Employee Name Input(self):
        """Input field for entering the employee's name."""
        return self.page.Employee Name*.or_(self.page.div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2) > input)

    @property
    def Status Dropdown(self):
        """Dropdown to select the user's status (Enabled or Disabled)."""
        return self.page.Status*.or_(self.page.div:nth-child(2) > div:nth-child(1) > div > div:nth-child(2) > i)

    @property
    def Username Input(self):
        """Input field for entering the username."""
        return self.page.Username*.or_(self.page.div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2) > input)

    @property
    def Password Input(self):
        """Input field for entering the password."""
        return self.page.Password*.or_(self.page.div:nth-child(3) > div:nth-child(1) > div > div:nth-child(2) > input)

    @property
    def Confirm Password Input(self):
        """Input field for confirming the password."""
        return self.page.Confirm Password*.or_(self.page.div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2) > input)

    @property
    def Cancel Button(self):
        """Button to cancel adding a new user."""
        return self.page.button.or_(self.page.Cancel)

    @property
    def Save Button(self):
        """Button to save the new user."""
        return self.page.button.or_(self.page.Save)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'OrangeHRM'
        await Header text is 'Add User'
        await The URL contains '/admin/saveSystemUser'