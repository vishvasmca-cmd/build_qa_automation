from playwright.async_api import Page, expect

class EmployeeListPage:
    """
    This page displays a list of employees and allows users to search, filter, and add new employees.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def employee_name_input(self):
        """Input field for entering the employee's name."""
        return self.page.//label[text()='Employee Name']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def employee_id_input(self):
        """Input field for entering the employee's ID."""
        return self.page.//label[text()='Employee Id']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def employment_status_dropdown(self):
        """Dropdown for selecting the employee's employment status."""
        return self.page.//label[text()='Employment Status']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--after)

    @property
    def include_dropdown(self):
        """Dropdown for selecting the employee's employment status."""
        return self.page.//label[text()='Include']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--after)

    @property
    def supervisor_name_input(self):
        """Input field for entering the supervisor's name."""
        return self.page.//label[text()='Supervisor Name']/following-sibling::input.or_(self.page.input[placeholder='Type for hints...'])

    @property
    def job_title_dropdown(self):
        """Dropdown for selecting the employee's job title."""
        return self.page.//label[text()='Job Title']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--after)

    @property
    def sub_unit_dropdown(self):
        """Dropdown for selecting the employee's sub unit."""
        return self.page.//label[text()='Sub Unit']/following-sibling::div//div[@class='oxd-select-text--after'].or_(self.page.div.oxd-select-text--after)

    @property
    def reset_button(self):
        """Button to reset the search filters."""
        return self.page.//button[text()=' Reset '].or_(self.page.button:contains('Reset'))

    @property
    def search_button(self):
        """Button to initiate the employee search."""
        return self.page.//button[text()=' Search '].or_(self.page.button:contains('Search'))

    @property
    def add_button(self):
        """Button to navigate to the add employee page."""
        return self.page.//button[contains(@class, 'oxd-button--success') and text()=' Add '].or_(self.page.button:contains('Add'))

    @property
    def employee_list_header(self):
        """Header displaying the title of the employee list section."""
        return self.page.//h6[text()='Employee Information'].or_(self.page.h6:contains('Employee Information'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'OrangeHRM'
        await Header text 'Employee Information' is displayed
        await The 'Add' button is present
        await The 'Search' button is present
        await The 'Reset' button is present
        await Employee Name input field is present
        await Employee Id input field is present
        await Employment Status dropdown is present
        await Include dropdown is present
        await Supervisor Name input field is present
        await Job Title dropdown is present
        await Sub Unit dropdown is present