from playwright.async_api import Page, expect

class AddEmployeePage:
    """
    This page is used to add a new employee to the OrangeHRM system.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name(self):
        """Input field for the employee's first name."""
        return self.page.ByRole('textbox', {'name': 'First Name'}).or_(self.page.ByCssSelector('input[name="firstName"]'))

    @property
    def middle_name(self):
        """Input field for the employee's middle name."""
        return self.page.ByRole('textbox', {'name': 'Middle Name'}).or_(self.page.ByCssSelector('input[name="middleName"]'))

    @property
    def last_name(self):
        """Input field for the employee's last name."""
        return self.page.ByRole('textbox', {'name': 'Last Name'}).or_(self.page.ByCssSelector('input[name="lastName"]'))

    @property
    def employee_id(self):
        """Input field for the employee's ID."""
        return self.page.ByRole('textbox', {'name': 'Employee Id'}).or_(self.page.ByCssSelector('div.oxd-form-row:nth-child(2) div.oxd-input-field-bottom-space > div > input'))

    @property
    def create_login_details_toggle(self):
        """Toggle to enable or disable creating login details for the new employee."""
        return self.page.ByRole('checkbox', {'name': 'Create Login Details'}).or_(self.page.ByCssSelector('span.oxd-switch-input'))

    @property
    def save_button(self):
        """Button to save the new employee's information."""
        return self.page.ByRole('button', {'name': 'Save'}).or_(self.page.ByText('Save'))

    @property
    def cancel_button(self):
        """Button to cancel adding a new employee."""
        return self.page.ByRole('button', {'name': 'Cancel'}).or_(self.page.ByText('Cancel'))

    @property
    def add_employee_header(self):
        """The header text of the Add Employee page."""
        return self.page.ByRole('heading', {'name': 'Add Employee'}).or_(self.page.ByText('Add Employee'))

    @property
    def profile_picture_upload(self):
        """Button to upload the employee's profile picture."""
        return self.page.ByRole('button').or_(self.page.ByCssSelector('div.orangehrm-employee-image > div > input[type=file]'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'OrangeHRM'
        await Header text is 'Add Employee'
        await Save button is present
        await First Name field is present