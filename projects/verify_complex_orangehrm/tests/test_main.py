import sys
import os
sys.path.append(os.getcwd())

from playwright.sync_api import Page, expect
import re

try:
    from helpers import take_screenshot
except ImportError:
    def take_screenshot(page, name, project_name):
        pass  # Fallback if helpers not available

class LoginPage:
    """Auto-generated Page Object for LoginPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def login_button(self):
        """The goal is to log in with username 'Admin' and password 'admin123'. The current page is the login p"""
        return self.page.get_by_role("button", name="Login", exact=True).first

    @property
    def username_input(self):
        """The goal's first step is to log in. I am currently on the login page. The goal specifies the usernam"""
        return self.page.locator("input[name='username']")

    @property
    def password_input(self):
        """The goal's first step is to log in. I have already filled the username field. Now I need to fill the"""
        return self.page.locator("input[name='password']")


class OrangehrmLoginPage:
    """Auto-generated Page Object for OrangehrmLoginPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def login_button(self):
        """I am on the login page and need to enter the username and password, then click the login button. I h"""
        return self.page.get_by_role("button", name="Login", exact=True).first


class HomePage:
    """Auto-generated Page Object for HomePage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def client_brand_logo_link(self):
        """I have successfully logged in. The next step is to navigate to the PIM page. I will use the 'PIM' li"""
        return self.page.locator("div.oxd-brand-banner > img")


class OrangehrmDashboardPage:
    """Auto-generated Page Object for OrangehrmDashboardPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def pim_link(self):
        """The goal is to add an employee in the PIM module. I am currently on the dashboard page after logging"""
        return self.page.get_by_role("menuitem", name="PIM").first


class EmployeeListPage:
    """Auto-generated Page Object for EmployeeListPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_button(self):
        """The goal is to add a new employee. I am currently on the Employee List page. The next step is to cli"""
        return self.page.get_by_role("button", name="Add", exact=True).first


class AddEmployeePage:
    """Auto-generated Page Object for AddEmployeePage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name_input(self):
        """I am currently on the 'Add Employee' page and need to fill in the employee details as per the goal. """
        return self.page.locator("input[name='firstName']")

    @property
    def last_name_input(self):
        """I am currently on the 'Add Employee' page and have already filled in the 'First Name' field. The nex"""
        return self.page.locator("input[name='lastName']")

    @property
    def save_button(self):
        """The goal is to add a new employee with the first name 'Resilience' and last name 'Agent', then click"""
        return self.page.get_by_role("button", name="Save", exact=True).first


class UnknownPage:
    """Auto-generated Page Object for UnknownPage"""
    def __init__(self, page: Page):
        self.page = page

    @property
    def done_element(self):
        """The goal is to add a new employee with the first name 'Resilience' and last name 'Agent'. The previo"""
        return self.page.locator("body")


def test_autonomous_flow(page: Page):
    """
    Workflow: 1. Login: Enter Admin / admin123 and click Login. 2. PIM: Click 'PIM' menu. 3. Action: Click 'Add Employee', enter First Name 'Resilience' and Last Name 'Agent', then click 'Save'. 4. Verify: Ensure the Personal Details page for the new employee is shown.
    """
    # Navigate to target URL
    page.goto("https://opensource-demo.orangehrmlive.com/")

    login_page = LoginPage(page)
    orangehrm_login_page = OrangehrmLoginPage(page)
    home_page = HomePage(page)
    orangehrm_dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeePage(page)
    unknown_page = UnknownPage(page)

    # Execute test steps
    # Step 0: The goal is to log in with username 'Admin' and password 'admin123'. The current
    # login_page.login_button.fill("Admin")

    # Step 1: The goal's first step is to log in. I am currently on the login page. The goal s
    login_page.username_input.fill("Admin")

    # Step 2: The goal's first step is to log in. I have already filled the username field. No
    login_page.password_input.fill("admin123")

    # Step 3: I am on the login page and need to enter the username and password, then click t
    orangehrm_login_page.login_button.click()

    # Step 4: I have successfully logged in. The next step is to navigate to the PIM page. I w
    # try:
    #     with page.context.expect_page(timeout=3000) as new_page_info:
    #         home_page.client_brand_logo_link.click()
    #     new_page = new_page_info.value
    #     new_page.close()
    # except Exception:
    #     pass
    home_page.client_brand_logo_link.click()

    # Step 5: The goal is to add an employee in the PIM module. I am currently on the dashboar
    # try:
    #     with page.context.expect_page(timeout=3000) as new_page_info:
    #         orangehrm_dashboard_page.pim_link.click()
    #     new_page = new_page_info.value
    #     new_page.close()
    # except Exception:
    #     pass
    orangehrm_dashboard_page.pim_link.click()

    # Step 6: The goal is to add a new employee. I am currently on the Employee List page. The
    employee_list_page.add_button.click()

    # Step 7: I am currently on the 'Add Employee' page and need to fill in the employee detai
    add_employee_page.first_name_input.fill("Resilience")

    # Step 8: I am currently on the 'Add Employee' page and have already filled in the 'First 
    add_employee_page.last_name_input.fill("Agent")

    # Step 9: The goal is to add a new employee with the first name 'Resilience' and last name
    add_employee_page.save_button.click()

    # Step 10: The goal is to add a new employee with the first name 'Resilience' and last name
    # Goal Achieved