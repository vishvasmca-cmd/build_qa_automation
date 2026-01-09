from playwright.async_api import Page, expect

class OrangehrmSystemUsersPage:
    """
    This page allows administrators to manage system users, including searching, adding, editing, and deleting users.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Username Filter(self):
        """Input field to filter users by username."""
        return self.page.[placeholder='Username'].or_(self.page.input[placeholder='Username'])

    @property
    def User Role Dropdown(self):
        """Dropdown to filter users by role."""
        return self.page.div:nth-child(2) > div > div.oxd-select-text.oxd-select-text--active.or_(self.page.div:nth-child(2) > div > div.oxd-select-text.oxd-select-text--active)

    @property
    def Employee Name Filter(self):
        """Input field to filter users by employee name."""
        return self.page.[placeholder='Type for hints...'].or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Status Dropdown(self):
        """Dropdown to filter users by status."""
        return self.page.div:nth-child(4) > div > div.oxd-select-text.oxd-select-text--active.or_(self.page.div:nth-child(4) > div > div.oxd-select-text.oxd-select-text--active)

    @property
    def Reset Button(self):
        """Button to reset the filter criteria."""
        return self.page.//button[text()=' Reset '].or_(self.page.button:contains('Reset'))

    @property
    def Search Button(self):
        """Button to apply the filter criteria."""
        return self.page.//button[text()=' Search '].or_(self.page.button:contains('Search'))

    @property
    def Add Button(self):
        """Button to navigate to the Add User page."""
        return self.page.//button[text()=' Add '].or_(self.page.button:contains('Add'))

    @property
    def Username Column Header(self):
        """Column header for Username."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][1]//i.or_(self.page.div.oxd-table-header-cell.oxd-padding-cell:nth-child(2))

    @property
    def User Role Column Header(self):
        """Column header for User Role."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][2]//i.or_(self.page.div.oxd-table-header-cell.oxd-padding-cell:nth-child(3))

    @property
    def Employee Name Column Header(self):
        """Column header for Employee Name."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][3]//i.or_(self.page.div.oxd-table-header-cell.oxd-padding-cell:nth-child(4))

    @property
    def Status Column Header(self):
        """Column header for Status."""
        return self.page.//div[@class='oxd-table-header-cell oxd-padding-cell'][4]//i.or_(self.page.div.oxd-table-header-cell.oxd-padding-cell:nth-child(5))

    @property
    def Delete Icon(self):
        """Delete icon for the first user in the table."""
        return self.page.//div[@class='oxd-table-body']/div[1]//button[1].or_(self.page.div.oxd-table-body > div:nth-child(1) button:nth-child(1))

    @property
    def Edit Icon(self):
        """Edit icon for the first user in the table."""
        return self.page.//div[@class='oxd-table-body']/div[1]//button[2].or_(self.page.div.oxd-table-body > div:nth-child(1) button:nth-child(2))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'OrangeHRM'
        await Header text is 'System Users'
        await Add button is present
        await Search button is present
        await Reset button is present
        await Table of users is displayed