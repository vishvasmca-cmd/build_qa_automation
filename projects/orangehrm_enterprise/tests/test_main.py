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
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    def go_to_login_page(self):
        self.navigate(self.url)

    def login(self, username, password):
        self.page.locator("[name='username']").fill(username)
        self.page.locator("[name='password']").fill(password)
        self.page.get_by_role("button", name="Login").click()

class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate_to_pim(self):
        self.page.get_by_role("link", name="PIM").click()

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_add_employee(self):
        self.page.get_by_role("button", name="Add").click()

class AddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def fill_employee_details(self, first_name, last_name):
        self.page.locator("[name='firstName']").fill(first_name)
        self.page.locator("[name='lastName']").fill(last_name)

    def click_save(self):
        self.page.get_by_role("button", name="Save").click()

class AdminPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate_to_admin(self):
        self.page.get_by_role("link", name="Admin").click()

    def navigate_to_system_users(self):
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers")
        self.page.wait_for_load_state("networkidle")

class SystemUsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_add_user(self):
        self.page.get_by_role("button", name="Add").click()

class AddUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def fill_employee_name(self, employee_name):
        self.page.get_by_placeholder("Type for hints...").fill(employee_name)
        self.page.get_by_placeholder("Type for hints...").fill(employee_name)

    def click_save(self):
        self.page.get_by_role("button", name="Save").click()

from playwright.sync_api import Browser

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeePage(page)
    admin_page = AdminPage(page)
    system_users_page = SystemUsersPage(page)
    add_user_page = AddUserPage(page)

    # Login
    login_page.go_to_login_page()
    login_page.login("Admin", "admin123")

    # Navigate to PIM module
    dashboard_page.navigate_to_pim()

    # Add Employee
    employee_list_page.click_add_employee()
    add_employee_page.fill_employee_details("FirstNameTest", "LastNameTest")
    add_employee_page.click_save()
    add_employee_page.click_save()

    # Navigate to Admin module
    admin_page.navigate_to_admin()
    admin_page.navigate_to_system_users()

    # Add User
    system_users_page.click_add_user()
    add_user_page.fill_employee_name("FirstNameTest LastNameTest")
    add_user_page.click_save()

    page.close()