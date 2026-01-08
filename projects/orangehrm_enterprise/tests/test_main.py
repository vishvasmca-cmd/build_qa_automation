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
        self.username_field = self.page.locator("[name='username']")
        self.password_field = self.page.locator("[name='password']")
        self.login_button = self.page.get_by_role("button", name="Login")

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()

class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_link = self.page.get_by_role("link", name="PIM")

    def navigate_to_pim(self):
        self.pim_link.click()

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button = self.page.get_by_role("button", name="Add")

    def navigate_to_add_employee(self):
        self.add_button.click()

class OrangehrmAddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_field = self.page.locator("[name='firstName']")
        self.last_name_field = self.page.locator("[name='lastName']")

    def fill_employee_details(self, first_name, last_name):
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)

from playwright.sync_api import Browser

# Corrected relative import
from projects.orangehrm_enterprise.pages.base_page import BasePage
from projects.orangehrm_enterprise.pages.login_page import LoginPage
from projects.orangehrm_enterprise.pages.dashboard_page import OrangehrmDashboardPage
from projects.orangehrm_enterprise.pages.employee_list_page import EmployeeListPage
from projects.orangehrm_enterprise.pages.add_employee_page import OrangehrmAddEmployeePage

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = OrangehrmAddEmployeePage(page)

    # 1. Login
    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.login("Admin", "admin123")
    page.wait_for_url("**/dashboard")

    # 2. Navigate to PIM
    dashboard_page.navigate_to_pim()
    page.wait_for_url("**/viewEmployeeList")

    # 3. Navigate to Add Employee
    employee_list_page.navigate_to_add_employee()
    page.wait_for_url("**/addEmployee")

    # 4. Fill Employee Details
    add_employee_page.fill_employee_details("FirstNameTest", "LastNameTest")

    # Take a screenshot
    take_screenshot(page, "add_employee_form_filled", "orangehrm_enterprise")

    page.close()