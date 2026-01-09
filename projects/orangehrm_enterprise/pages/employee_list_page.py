from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    This is the Employee List page within the PIM module, where users can view, search, and manage employee records.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Employee Name Input(self):
        """Input field for filtering employees by name."""
        return self.page.//label[text()='Employee Name']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Employee Id Input(self):
        """Input field for filtering employees by ID."""
        return self.page.//label[text()='Employee Id']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Employment Status Dropdown(self):
        """Dropdown to filter employees by employment status."""
        return self.page.//label[text()='Employment Status']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text-input)

    @property
    def Include Dropdown(self):
        """Dropdown to filter employees by inclusion criteria (e.g., Current Employees Only)."""
        return self.page.//label[text()='Include']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text-input)

    @property
    def Supervisor Name Input(self):
        """Input field for filtering employees by supervisor name."""
        return self.page.//label[text()='Supervisor Name']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Job Title Dropdown(self):
        """Dropdown to filter employees by job title."""
        return self.page.//label[text()='Job Title']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text-input)

    @property
    def Sub Unit Dropdown(self):
        """Dropdown to filter employees by sub unit."""
        return self.page.//label[text()='Sub Unit']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text-input)

    @property
    def Reset Button(self):
        """Button to reset the filter criteria."""
        return self.page.//button[text()=' Reset '].or_(self.page.button:contains('Reset'))

    @property
    def Search Button(self):
        """Button to apply the filter criteria and search for employees."""
        return self.page.//button[text()=' Search '].or_(self.page.button:contains('Search'))

    @property
    def Add Button(self):
        """Button to navigate to the Add Employee page."""
        return self.page.//button[contains(@class, 'oxd-button--success') and contains(text(), 'Add')].or_(self.page.button:contains('Add'))

    @property
    def Employee List Table(self):
        """Table displaying the list of employees."""
        return self.page.//div[@class='oxd-table-body'].or_(self.page.div.oxd-table-body)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'OrangeHRM'
        await Header text is 'Employee Information'
        await The 'Add' button is present
        await The 'Search' button is present
        await The employee list table is displayed