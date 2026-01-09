from playwright.async_api import Page, expect

class AddEmployeeOrangehrmPage:
    """
    This page is used to add a new employee to the OrangeHRM system.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Add Employee Header(self):
        """The main header of the Add Employee page."""
        return self.page.text=Add Employee.or_(self.page.css=.orangehrm-card-title)

    @property
    def First Name Input(self):
        """Input field for the employee's first name."""
        return self.page.placeholder=First Name.or_(self.page.css=input[name='firstName'])

    @property
    def Middle Name Input(self):
        """Input field for the employee's middle name."""
        return self.page.placeholder=Middle Name.or_(self.page.css=input[name='middleName'])

    @property
    def Last Name Input(self):
        """Input field for the employee's last name."""
        return self.page.placeholder=Last Name.or_(self.page.css=input[name='lastName'])

    @property
    def Employee Id Input(self):
        """Input field for the employee's ID."""
        return self.page.css=div.oxd-grid-item:nth-child(1) > div:nth-child(1) > div:nth-child(2) > input.or_(self.page.name=employeeId)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Assert that the page title is 'OrangeHRM'
        await Assert that the 'Add Employee' header is displayed
        await Assert that the First Name input field is present
        await Assert that the Last Name input field is present