from playwright.async_api import Page, expect

class UnknownPage:
    """
    This page appears to be a registration or signup page for a service or application.
    URL Pattern: /register
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name_input(self):
        """Input field for the user's first name."""
        return self.page.get_by_role('textbox', name='First name').or_(self.page.locator('#firstName'))

    @property
    def last_name_input(self):
        """Input field for the user's last name."""
        return self.page.get_by_role('textbox', name='Last name').or_(self.page.locator('#lastName'))

    @property
    def email_input(self):
        """Input field for the user's email address."""
        return self.page.get_by_role('textbox', name='Email').or_(self.page.locator('#userEmail'))

    @property
    def mobile_input(self):
        """Input field for the user's mobile number."""
        return self.page.get_by_role('textbox', name='Mobile').or_(self.page.locator('#userNumber'))

    @property
    def date_of_birth_input(self):
        """Input field for the user's date of birth."""
        return self.page.locator('#dateOfBirthInput').or_(self.page.locator('#dateOfBirth'))

    @property
    def gender_radio_button_male(self):
        """Radio button for selecting Male gender."""
        return self.page.get_by_role('radio', name='Male').or_(self.page.locator('#gender-radio-1'))

    @property
    def gender_radio_button_female(self):
        """Radio button for selecting Female gender."""
        return self.page.get_by_role('radio', name='Female').or_(self.page.locator('#gender-radio-2'))

    @property
    def hobbies_checkbox_sports(self):
        """Checkbox for selecting Sports as a hobby."""
        return self.page.get_by_role('checkbox', name='Sports').or_(self.page.locator('#hobbies-checkbox-1'))

    @property
    def hobbies_checkbox_reading(self):
        """Checkbox for selecting Reading as a hobby."""
        return self.page.get_by_role('checkbox', name='Reading').or_(self.page.locator('#hobbies-checkbox-2'))

    @property
    def hobbies_checkbox_music(self):
        """Checkbox for selecting Music as a hobby."""
        return self.page.get_by_role('checkbox', name='Music').or_(self.page.locator('#hobbies-checkbox-3'))

    @property
    def current_address_textarea(self):
        """Text area for entering the user's current address."""
        return self.page.locator('#currentAddress').or_(self.page.get_by_placeholder('Current Address'))

    @property
    def select_state(self):
        """Dropdown for selecting the user's state."""
        return self.page.locator('#state').or_(self.page.locator('#react-select-3-input'))

    @property
    def select_city(self):
        """Dropdown for selecting the user's city."""
        return self.page.locator('#city').or_(self.page.locator('#react-select-4-input'))

    @property
    def submit_button(self):
        """Button to submit the registration form."""
        return self.page.get_by_role('button', name='Submit').or_(self.page.locator('#submit'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(page).to_have_title('ToolsQA')
        await expect(page.get_by_text('Student Registration Form')).to_be_visible()
        await expect(page.locator('#firstName')).to_be_visible()
        await expect(page.locator('#lastName')).to_be_visible()
        await expect(page.locator('#userEmail')).to_be_visible()
        await expect(page.locator('#userNumber')).to_be_visible()
        await expect(page.locator('#currentAddress')).to_be_visible()
        await expect(page.locator('#submit')).to_be_visible()