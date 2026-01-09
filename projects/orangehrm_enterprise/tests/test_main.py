# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('C:/Users/vishv/.gemini/antigravity/playground/inner-event/core/lib/templates')
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
        self.page = page

    def navigate(self):
        super().navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    def login(self, username, password):
        self.page.locator("[name='username']").fill(username)
        self.page.locator("[name='password']").fill(password)
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_url("**/dashboard*")


class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate_to_pim(self):
        self.page.get_by_role("link", name="PIM").click()
        self.page.wait_for_url("**/viewEmployeeList*")

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def click_add(self):
        self.page.get_by_role("button", name="Add").click()
        self.page.wait_for_url("**/addEmployee*")

class AddEmployeeOrangehrmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def add_employee(self, first_name, last_name):
        self.page.locator("[name='firstName']").fill(first_name)
        self.page.locator("[name='lastName']").fill(last_name)
        self.page.get_by_role("button", name="Save").click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_admin(self):
        self.page.get_by_role("link", name="Admin").click()
        self.page.wait_for_url("**/viewSystemUsers*")

class PimPersonalDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

class OrangehrmSystemUsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def click_add(self):
        self.page.get_by_role("button", name="Add").click()
        self.page.wait_for_url("**/saveSystemUser*")

class AddUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def add_user(self, employee_name):
        self.page.get_by_placeholder("Type for hints...").fill(employee_name)
        self.page.locator(".oxd-autocomplete-dropdown.--positon-bottom").locator(".oxd-autocomplete-option").first.click()
        self.page.get_by_role("button", name="Save").click()
        self.page.wait_for_load_state("networkidle")

def test_autonomous_flow(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeeOrangehrmPage(page)
    pim_personal_details_page = PimPersonalDetailsPage(page)
    system_users_page = OrangehrmSystemUsersPage(page)
    add_user_page = AddUserPage(page)

    # 1. Login
    login_page.navigate()
    login_page.login("Admin", "admin123")

    # 2. Navigate to PIM module and Add a new employee (FirstNameTest LastNameTest)
    dashboard_page.navigate_to_pim()
    employee_list_page.click_add()
    add_employee_page.add_employee("FirstNameTest", "LastNameTest")

    # 3. Navigate to Admin module -> User Management -> Users
    add_employee_page.navigate_to_admin()
    system_users_page.click_add()

    # 4. Create a System User for the newly created employee.
    add_user_page.add_user("FirstNameTest LastNameTest")
