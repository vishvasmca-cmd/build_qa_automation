from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    This page displays a list of employees and allows filtering and adding new employees.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Employee Name Filter(self):
        """Input field to filter employees by name."""
        return self.page.placeholder="Type for hints...".or_(self.page.css=div.oxd-input-field:nth-child(1) > div > input)

    @property
    def Employee Id Filter(self):
        """Input field to filter employees by ID."""
        return self.page.placeholder="Type for hints...".or_(self.page.css=div.oxd-input-field:nth-child(2) > div > input)

    @property
    def Employment Status Filter(self):
        """Dropdown to filter employees by employment status."""
        return self.page.text=-- Select --.or_(self.page.css=div.oxd-input-field:nth-child(3) > div > div.oxd-select-wrapper > div.oxd-select-text)

    @property
    def Include Filter(self):
        """Dropdown to filter employees by inclusion status."""
        return self.page.text=Current Employees Only.or_(self.page.css=div.oxd-input-field:nth-child(4) > div > div.oxd-select-wrapper > div.oxd-select-text)

    @property
    def Supervisor Name Filter(self):
        """Input field to filter employees by supervisor name."""
        return self.page.placeholder="Type for hints...".or_(self.page.css=div.oxd-input-field:nth-child(5) > div > input)

    @property
    def Job Title Filter(self):
        """Dropdown to filter employees by job title."""
        return self.page.text=-- Select --.or_(self.page.css=div.oxd-input-field:nth-child(6) > div > div.oxd-select-wrapper > div.oxd-select-text)

    @property
    def Sub Unit Filter(self):
        """Dropdown to filter employees by sub unit."""
        return self.page.text=-- Select --.or_(self.page.css=div.oxd-input-field:nth-child(7) > div > div.oxd-select-wrapper > div.oxd-select-text)

    @property
    def Reset Button(self):
        """Button to reset the filter criteria."""
        return self.page.text=Reset.or_(self.page.css=button.oxd-button--ghost)

    @property
    def Search Button(self):
        """Button to apply the filter criteria."""
        return self.page.text=Search.or_(self.page.css=button.oxd-button--main)

    @property
    def Add Button(self):
        """Button to navigate to the Add Employee page."""
        return self.page.text=Add.or_(self.page.css=button.oxd-button--success)

    @property
    def PIM Menu Item(self):
        """Menu item to navigate to the PIM section."""
        return self.page.text=PIM.or_(self.page.css=li.oxd-main-menu-item--active > a > span.oxd-text)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Assert that the page title contains 'Employee List'
        await Assert that the 'Employee Information' header is displayed
        await Assert that the 'Add' button is displayed
        await Assert that the employee table is displayed
        await Assert that the URL contains '/pim/viewEmployeeList'