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

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_locator = "[name='username']"
        self.password_locator = "[name='password']"
        self.login_button_locator = "page.get_by_role(\"button\", name=\"Login\")"

    def login(self, username, password):
        self.page.locator(self.username_locator).fill(username)
        self.page.locator(self.password_locator).fill(password)
        self.page.locator(self.login_button_locator).click()

class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_link_locator = "page.get_by_role(\"link\", name=\"PIM\")"

    def navigate_to_pim(self):
        self.page.locator(self.pim_link_locator).click()

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = "page.get_by_role(\"button\", name=\"Add\")"

    def navigate_to_add_employee(self):
        self.page.locator(self.add_button_locator).click()

class AddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_locator = "[name='firstName']"
        self.last_name_locator = "[name='lastName']"
        self.save_button_locator = "page.get_by_role(\"button\", name=\"Save\")"

    def add_employee(self, first_name, last_name):
        self.page.locator(self.first_name_locator).fill(first_name)
        self.page.locator(self.last_name_locator).fill(last_name)
        self.page.locator(self.save_button_locator).click()

    def click_save(self):
        self.page.locator(self.save_button_locator).click()

class AdminPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.admin_link_locator = "page.get_by_role(\"link\", name=\"Admin\")"

    def navigate_to_admin(self):
        self.page.locator(self.admin_link_locator).click()

class SystemUsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = "page.get_by_role(\"button\", name=\"Add\")"

    def navigate_to_add_user(self):
        self.page.locator(self.add_button_locator).click()

class AddUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.employee_name_locator = "page.get_by_placeholder(\"Type for hints...\")"
        self.save_button_locator = "page.get_by_role(\"button\", name=\"Save\")"

    def add_user(self, employee_name):
        self.page.locator(self.employee_name_locator).fill(employee_name)
        self.page.locator(self.employee_name_locator).fill(employee_name)
        self.page.locator(self.save_button_locator).click()

from playwright.sync_api import Browser
from projects.orangehrm_enterprise.pages.base_page import BasePage
from projects.orangehrm_enterprise.pages.login_page import LoginPage
from projects.orangehrm_enterprise.pages.orangehrm_dashboard_page import OrangehrmDashboardPage
from projects.orangehrm_enterprise.pages.employee_list_page import EmployeeListPage
from projects.orangehrm_enterprise.pages.add_employee_page import AddEmployeePage
from projects.orangehrm_enterprise.pages.admin_page import AdminPage
from projects.orangehrm_enterprise.pages.system_users_page import SystemUsersPage
from projects.orangehrm_enterprise.pages.add_user_page import AddUserPage

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    base_url = "https://opensource-demo.orangehrmlive.com/web/index.php"

    # Initialize pages
    base_page = BasePage(page)
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeePage(page)
    admin_page = AdminPage(page)
    system_users_page = SystemUsersPage(page)
    add_user_page = AddUserPage(page)

    # Login
    base_page.navigate(base_url + "/auth/login")
    login_page.login("Admin", "admin123")

    # Add Employee
    dashboard_page.navigate_to_pim()
    employee_list_page.navigate_to_add_employee()
    add_employee_page.add_employee("FirstNameTest", "LastNameTest")
    add_employee_page.click_save()
    add_employee_page.click_save()

    # Add System User
    admin_page.navigate_to_admin()
    page.goto(base_url + "/admin/viewSystemUsers")
    system_users_page.navigate_to_add_user()
    add_user_page.add_user("FirstNameTest LastNameTest")

    page.close()