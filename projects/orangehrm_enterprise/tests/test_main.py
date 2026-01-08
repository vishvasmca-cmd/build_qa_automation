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
        self.page = page

    def enter_username(self, username):
        self.page.locator("[name='username']").fill(username)

    def enter_password(self, password):
        self.page.locator("[name='password']").fill(password)

    def click_login(self):
        self.page.get_by_role("button", name="Login").click()


class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate_to_pim(self):
        self.page.get_by_role("link", name="PIM").click()


class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def click_add(self):
        self.page.get_by_role("button", name="Add").click()


class AddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def enter_first_name(self, first_name):
        self.page.locator("[name='firstName']").fill(first_name)

    def enter_last_name(self, last_name):
        self.page.locator("[name='lastName']").fill(last_name)

    def click_save(self):
        self.page.get_by_role("button", name="Save").click()


class SystemUsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def click_add(self):
        self.page.get_by_role("button", name="Add").click()


class AddUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def enter_employee_name(self, employee_name):
        self.page.get_by_placeholder("Type for hints...").fill(employee_name)

    def select_employee_name(self, employee_name):
        self.page.get_by_text(employee_name, exact=True).click()

    def click_save(self):
        self.page.get_by_role("button", name="Save").click()


class OrangehrmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate_to_admin(self):
        self.page.get_by_role("link", name="Admin").click()


from playwright.sync_api import Browser, expect

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeePage(page)
    system_users_page = SystemUsersPage(page)
    add_user_page = AddUserPage(page)
    orangehrm_page = OrangehrmPage(page)

    # Login
    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.enter_username("Admin")
    login_page.enter_password("admin123")
    login_page.click_login()
    expect(page).to_have_url("**/dashboard")

    # Navigate to PIM module
    dashboard_page.navigate_to_pim()
    expect(page).to_have_url("**/pim/viewEmployeeList")

    # Add a new employee
    employee_list_page.click_add()
    expect(page).to_have_url("**/pim/addEmployee")
    add_employee_page.enter_first_name("FirstNameTest")
    add_employee_page.enter_last_name("LastNameTest")
    add_employee_page.click_save()
    add_employee_page.click_save()

    # Navigate to Admin module
    orangehrm_page.navigate_to_admin()
    expect(page).to_have_url("**/admin/viewSystemUsers")

    # Create a system user
    system_users_page.click_add()
    expect(page).to_have_url("**/admin/saveSystemUser")
    employee_name = "FirstNameTest LastNameTest"
    add_user_page.enter_employee_name(employee_name)
    add_user_page.select_employee_name(employee_name)
    add_user_page.click_save()
