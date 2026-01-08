from playwright.async_api import Page, expect

class EmployeeListOrangehrmPage:
    """
    Employee List page in OrangeHRM
    URL Pattern: /pim/addEmployee
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Employee Name Input(self):
        """Input field for employee name"""
        return self.page.get_by_placeholder('Type for hints...').or_(self.page.locator('input[placeholder="Type for hints..."]').first)

    @property
    def Employee ID Input(self):
        """Input field for employee ID"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(1).or_(self.page.locator('div.oxd-input-group').nth(1) input)

    @property
    def Employment Status Dropdown(self):
        """Dropdown for selecting employment status"""
        return self.page.locator('div.oxd-select-text--after i').or_(self.page.locator('div.oxd-input-group').nth(2) div.oxd-select-text)

    @property
    def Include Dropdown(self):
        """Dropdown for selecting include options"""
        return self.page.locator('div.oxd-select-text--after i').nth(1).or_(self.page.locator('div.oxd-input-group').nth(3) div.oxd-select-text)

    @property
    def Supervisor Name Input(self):
        """Input field for supervisor name"""
        return self.page.locator('input[placeholder="Type for hints..."]').nth(2).or_(self.page.locator('div.oxd-input-group').nth(4) input)

    @property
    def Job Title Dropdown(self):
        """Dropdown for selecting job title"""
        return self.page.locator('div.oxd-select-text--after i').nth(2).or_(self.page.locator('div.oxd-input-group').nth(5) div.oxd-select-text)

    @property
    def Sub Unit Dropdown(self):
        """Dropdown for selecting sub unit"""
        return self.page.locator('div.oxd-select-text--after i').nth(3).or_(self.page.locator('div.oxd-input-group').nth(6) div.oxd-select-text)

    @property
    def Reset Button(self):
        """Button to reset the search filters"""
        return self.page.get_by_role('button', name='Reset').or_(self.page.locator('button.oxd-button--ghost'))

    @property
    def Search Button(self):
        """Button to search employees"""
        return self.page.get_by_role('button', name='Search').or_(self.page.locator('button.oxd-button--secondary'))

    @property
    def Add Button(self):
        """Button to add a new employee"""
        return self.page.get_by_role('button', name=' Add ').or_(self.page.locator('button.oxd-button--success'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('OrangeHRM')
        await expect(page.locator('h6.oxd-text--h6').first).to_have_text('Employee Information')
        await expect(page.locator('span.oxd-topbar-header-breadcrumb > h6')).to_have_text('PIM')