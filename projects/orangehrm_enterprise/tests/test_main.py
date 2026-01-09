# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/lib/templates')
from helpers import take_screenshot


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name, project_name):
        take_screenshot(self.page, name, project_name)

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_locator = "[name='username']"
        self.password_locator = "[name='password']"
        self.login_button_locator = "Login"

    def login(self, username, password):
        self.page.locator(self.username_locator).fill(username)
        self.page.locator(self.password_locator).fill(password)
        self.page.get_by_role("button", name=self.login_button_locator).click()
        self.page.wait_for_url("**/dashboard*")

class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_link_locator = "PIM"

    def navigate_to_pim(self):
        self.page.get_by_role("link", name=self.pim_link_locator).click()
        self.page.wait_for_url("**/pim/viewEmployeeList*")

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = "Add"

    def navigate_to_add_employee(self):
        self.page.get_by_role("button", name=self.add_button_locator).click()
        self.page.wait_for_url("**/pim/addEmployee*")

class AddEmployeeOrangehrmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_locator = "[name='firstName']"
        self.last_name_locator = "[name='lastName']"
        self.save_button_locator = "Save"

    def add_employee(self, first_name, last_name):
        self.page.locator(self.first_name_locator).fill(first_name)
        self.page.locator(self.last_name_locator).fill(last_name)
        self.page.get_by_role("button", name=self.save_button_locator).click()
        self.page.wait_for_load_state("networkidle")

    def save_employee(self):
        self.page.get_by_role("button", name=self.save_button_locator).click()
        self.page.wait_for_load_state("networkidle")

class OrangehrmPimPersonalDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.admin_link_locator = "Admin"

    def navigate_to_admin(self):
        self.page.get_by_role("link", name=self.admin_link_locator).click()
        self.page.wait_for_url("**/admin/viewSystemUsers*")

class SystemUsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = "Add"

    def navigate_to_add_user(self):
        self.page.get_by_role("button", name=self.add_button_locator).click()
        self.page.wait_for_url("**/admin/saveSystemUser*")

class AddUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.employee_name_locator = "Type for hints..."
        self.save_button_locator = "Save"
        self.cancel_button_locator = "Cancel"

    def fill_employee_name(self, employee_name):
        self.page.get_by_placeholder(self.employee_name_locator).fill(employee_name)

    def save_user(self):
        self.page.get_by_role("button", name=self.save_button_locator).click()
        self.page.wait_for_load_state("networkidle")

    def cancel_add_user(self):
        self.page.get_by_role("button", name=self.cancel_button_locator).click()
        self.page.wait_for_url("**/admin/viewSystemUsers*")

class GenericPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

from playwright.sync_api import Browser

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    orangehrm_dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeeOrangehrmPage(page)
    orangehrm_pim_personal_details_page = OrangehrmPimPersonalDetailsPage(page)
    system_users_page = SystemUsersPage(page)
    add_user_page = AddUserPage(page)
    generic_page = GenericPage(page)

    # 1. Login
    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.login("Admin", "admin123")

    # 2. Navigate to PIM
    orangehrm_dashboard_page.navigate_to_pim()

    # 3. Add Employee
    employee_list_page.navigate_to_add_employee()
    add_employee_page.add_employee("FirstNameTest", "LastNameTest")

    # 4. Save Employee
    add_employee_page.save_employee()

    # 5. Navigate to Admin
    orangehrm_pim_personal_details_page.navigate_to_admin()

    # 6. Navigate to Add User
    system_users_page.navigate_to_add_user()

    # 7. Fill Employee Name
    add_user_page.fill_employee_name("Type for hints...")

    # 8. Save User
    add_user_page.save_user()

    # 9. Cancel Add User
    add_user_page.cancel_add_user()

    # 10. Navigate to Add User again
    system_users_page.navigate_to_add_user()

    # 11. Save User again
    add_user_page.save_user()

    page.close()