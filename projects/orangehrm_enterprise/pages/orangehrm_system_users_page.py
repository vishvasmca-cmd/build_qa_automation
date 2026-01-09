from playwright.async_api import Page, expect

class OrangehrmSystemUsersPage:
    """
    This page allows administrators to manage system users, including searching, adding, editing, and deleting users.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Filter(self):
        """Input field to filter users by username."""
        return self.page.//label[text()='Username']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def User Role Dropdown(self):
        """Dropdown to filter users by role."""
        return self.page.//label[text()='User Role']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--arrow)

    @property
    def Employee Name Filter(self):
        """Input field to filter users by employee name."""
        return self.page.//label[text()='Employee Name']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Status Dropdown(self):
        """Dropdown to filter users by status."""
        return self.page.//label[text()='Status']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--arrow)

    @property
    def Reset Button(self):
        """Button to reset the filter criteria."""
        return self.page.//button[text()=' Reset '].or_(self.page.button.oxd-button--ghost)

    @property
    def Search Button(self):
        """Button to apply the filter criteria."""
        return self.page.//button[text()=' Search '].or_(self.page.button.oxd-button--main)

    @property
    def Add Button(self):
        """Button to navigate to the Add User page."""
        return self.page.//button[text()=' Add '].or_(self.page.button.oxd-button--success)

    @property
    def Username Column Header(self):
        """Column header for Username."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][1]//i.or_(self.page.//div[text()='Username'])

    @property
    def User Role Column Header(self):
        """Column header for User Role."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][2]//i.or_(self.page.//div[text()='User Role'])

    @property
    def Employee Name Column Header(self):
        """Column header for Employee Name."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][3]//i.or_(self.page.//div[text()='Employee Name'])

    @property
    def Status Column Header(self):
        """Column header for Status."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][4]//i.or_(self.page.//div[text()='Status'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'OrangeHRM'
        await Header text is 'System Users'
        await Add button is displayed
        await Search button is displayed
        await Reset button is displayed