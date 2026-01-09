from playwright.async_api import Page, expect

class PimPersonalDetailsPage:
    """
    This page allows users to view and modify the personal details of an employee.
    URL Pattern: https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewPersonalDetails/empNumber/*
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def First Name(self):
        """Input field for the employee's first name."""
        return self.page.[name='firstName'].or_(self.page.input[placeholder='First Name'])

    @property
    def Middle Name(self):
        """Input field for the employee's middle name."""
        return self.page.[name='middleName'].or_(self.page.input[placeholder='Middle Name'])

    @property
    def Last Name(self):
        """Input field for the employee's last name."""
        return self.page.[name='lastName'].or_(self.page.input[placeholder='Last Name'])

    @property
    def Employee Id(self):
        """Input field for the employee's ID."""
        return self.page.[name='employeeId'].or_(self.page.div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > input)

    @property
    def Other Id(self):
        """Input field for the employee's other ID."""
        return self.page.[name='otherId'].or_(self.page.div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > input)

    @property
    def Driver's License Number(self):
        """Input field for the employee's driver's license number."""
        return self.page.[name='driverLicenseNo'].or_(self.page.div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div > input)

    @property
    def License Expiry Date(self):
        """Input field for the employee's license expiry date."""
        return self.page.[placeholder='yyyy-dd-mm'].or_(self.page.div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div > input)

    @property
    def Nationality(self):
        """Dropdown for selecting the employee's nationality."""
        return self.page.div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(1).or_(self.page.div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(1))

    @property
    def Marital Status(self):
        """Dropdown for selecting the employee's marital status."""
        return self.page.div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(1).or_(self.page.div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(1))

    @property
    def Date of Birth(self):
        """Input field for the employee's date of birth."""
        return self.page.[placeholder='yyyy-dd-mm'].or_(self.page.div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div > input)

    @property
    def Male Gender(self):
        """Radio button for selecting male gender."""
        return self.page.[value='1'].or_(self.page.div:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > label)

    @property
    def Female Gender(self):
        """Radio button for selecting female gender."""
        return self.page.[value='2'].or_(self.page.div:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(2) > label)

    @property
    def Save Button(self):
        """Button to save the personal details."""
        return self.page.button[type='submit'].or_(self.page.button:has-text('Save'))

    @property
    def Personal Details Tab(self):
        """Link to the Personal Details tab."""
        return self.page.text=Personal Details.or_(self.page.a:has-text('Personal Details'))

    @property
    def Contact Details Tab(self):
        """Link to the Contact Details tab."""
        return self.page.text=Contact Details.or_(self.page.a:has-text('Contact Details'))

    @property
    def Emergency Contacts Tab(self):
        """Link to the Emergency Contacts tab."""
        return self.page.text=Emergency Contacts.or_(self.page.a:has-text('Emergency Contacts'))

    @property
    def Dependents Tab(self):
        """Link to the Dependents tab."""
        return self.page.text=Dependents.or_(self.page.a:has-text('Dependents'))

    @property
    def Immigration Tab(self):
        """Link to the Immigration tab."""
        return self.page.text=Immigration.or_(self.page.a:has-text('Immigration'))

    @property
    def Job Tab(self):
        """Link to the Job tab."""
        return self.page.text=Job.or_(self.page.a:has-text('Job'))

    @property
    def Salary Tab(self):
        """Link to the Salary tab."""
        return self.page.text=Salary.or_(self.page.a:has-text('Salary'))

    @property
    def Report-to Tab(self):
        """Link to the Report-to tab."""
        return self.page.text=Report-to.or_(self.page.a:has-text('Report-to'))

    @property
    def Qualifications Tab(self):
        """Link to the Qualifications tab."""
        return self.page.text=Qualifications.or_(self.page.a:has-text('Qualifications'))

    @property
    def Memberships Tab(self):
        """Link to the Memberships tab."""
        return self.page.text=Memberships.or_(self.page.a:has-text('Memberships'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Assert that the page title contains 'OrangeHRM'
        await Assert that the 'Personal Details' header is displayed
        await Assert that the 'First Name' field is present
        await Assert that the 'Save' button is present