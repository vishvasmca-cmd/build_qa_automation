from playwright.async_api import Page, expect

class UnknownPage:
    """
    This is the Employee List page within the PIM module, where users can view, search, and manage employee information.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Employee Name Input(self):
        """Input field to search for employees by name."""
        return self.page.//label[text()='Employee Name']/following-sibling::div/input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Employee Id Input(self):
        """Input field to search for employees by ID."""
        return self.page.//label[text()='Employee Id']/following-sibling::div/input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Employment Status Dropdown(self):
        """Dropdown to filter employees by employment status."""
        return self.page.//label[text()='Employment Status']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--arrow)

    @property
    def Include Dropdown(self):
        """Dropdown to filter employees by inclusion criteria (e.g., Current Employees Only)."""
        return self.page.//label[text()='Include']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--arrow)

    @property
    def Supervisor Name Input(self):
        """Input field to search for employees by supervisor name."""
        return self.page.//label[text()='Supervisor Name']/following-sibling::div/input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def Job Title Dropdown(self):
        """Dropdown to filter employees by job title."""
        return self.page.//label[text()='Job Title']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--arrow)

    @property
    def Sub Unit Dropdown(self):
        """Dropdown to filter employees by sub unit."""
        return self.page.//label[text()='Sub Unit']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--arrow)

    @property
    def Reset Button(self):
        """Button to reset the search filters."""
        return self.page.//button[text()=' Reset '].or_(self.page.button.oxd-button--ghost)

    @property
    def Search Button(self):
        """Button to initiate the employee search."""
        return self.page.//button[text()=' Search '].or_(self.page.button.oxd-button--main)

    @property
    def Add Button(self):
        """Button to add a new employee."""
        return self.page.//button[normalize-space()='+ Add'].or_(self.page.button.oxd-button--success)

    @property
    def Edit Button(self):
        """Button to edit an employee."""
        return self.page.//div[@class='oxd-table-body']/div/div/div[@class='oxd-table-cell oxd-padding-cell'][last()]/div/button[1].or_(self.page.button.oxd-icon-button)

    @property
    def Delete Button(self):
        """Button to delete an employee."""
        return self.page.//div[@class='oxd-table-body']/div/div/div[@class='oxd-table-cell oxd-padding-cell'][last()]/div/button[2].or_(self.page.button.oxd-icon-button)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Assert page title contains 'Employee List'
        await Assert header text is 'Employee Information'
        await Assert that the 'Add' button is displayed
        await Assert that the 'Search' button is displayed
        await Assert that the 'Reset' button is displayed
        await Assert that the table of employees is displayed