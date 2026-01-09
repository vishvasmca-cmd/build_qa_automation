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
        self.username_locator = self.page.locator("[name='username']")
        self.password_locator = self.page.locator("[name='password']")
        self.login_button_locator = self.page.get_by_role("button", name="Login")

    def enter_username(self, username):
        self.username_locator.fill(username)

    def enter_password(self, password):
        self.password_locator.fill(password)

    def click_login(self):
        self.login_button_locator.click()


class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_link_locator = self.page.get_by_role("link", name="PIM")

    def navigate_to_pim(self):
        self.pim_link_locator.click()


class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = self.page.get_by_role("button", name="Add")

    def click_add(self):
        self.add_button_locator.click()


class AddEmployeeOrangehrmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_locator = self.page.locator("[name='firstName']")
        self.last_name_locator = self.page.locator("[name='lastName']")
        self.save_button_locator = self.page.get_by_role("button", name="Save")
        self.admin_link_locator = self.page.get_by_role("link", name="Admin")

    def enter_first_name(self, first_name):
        self.first_name_locator.fill(first_name)

    def enter_last_name(self, last_name):
        self.last_name_locator.fill(last_name)

    def click_save(self):
        self.save_button_locator.click()

    def navigate_to_admin(self):
        self.admin_link_locator.click()


class OrangehrmSystemUsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = self.page.get_by_role("button", name="Add")

    def click_add(self):
        self.add_button_locator.click()


class AddUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.employee_name_locator = self.page.get_by_placeholder("Type for hints...")
        self.save_button_locator = self.page.get_by_role("button", name="Save")
        self.user_role_dropdown_locator = self.page.get_by_text("-- Select --").first
        #self.user_role_dropdown_locator = self.page.locator("div[class*='oxd-select-text-input']").first
        self.admin_role_option_locator = self.page.get_by_role("option", name="Admin")
        self.status_dropdown_locator = self.page.locator("div:nth-child(3) > div > div:nth-child(2) > div > div[class*='oxd-select-text-input']").first
        self.enabled_status_option_locator = self.page.get_by_role("option", name="Enabled")

        self.username_locator = self.page.locator("div:nth-child(4) > div > div:nth-child(2) > input")
        self.password_locator = self.page.locator("div:nth-child(5) > div > div:nth-child(2) > input")
        self.confirm_password_locator = self.page.locator("div:nth-child(6) > div > div:nth-child(2) > input")

    def enter_employee_name(self, employee_name):
        self.employee_name_locator.fill(employee_name)
        self.page.locator(".oxd-autocomplete-dropdown.--positon-bottom").locator("span").click()

    def click_save(self):
        self.save_button_locator.click()

    def select_user_role(self, role):
        self.user_role_dropdown_locator.click()
        self.page.get_by_role("option", name=role).click()

    def select_status(self, status):
        self.status_dropdown_locator.click()
        self.page.get_by_role("option", name=status).click()

    def enter_username(self, username):
        self.username_locator.fill(username)

    def enter_password(self, password):
        self.password_locator.fill(password)

    def enter_confirm_password(self, confirm_password):
        self.confirm_password_locator.fill(confirm_password)


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeeOrangehrmPage(page)
    system_users_page = OrangehrmSystemUsersPage(page)
    add_user_page = AddUserPage(page)

    # 1. Login
    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.enter_username("Admin")
    login_page.enter_password("admin123")
    login_page.click_login()
    page.wait_for_url("**/dashboard*", timeout=60000)

    # 2. Navigate to PIM module and Add a new employee (FirstNameTest LastNameTest)
    dashboard_page.navigate_to_pim()
    employee_list_page.click_add()
    add_employee_page.enter_first_name("FirstNameTest")
    add_employee_page.enter_last_name("LastNameTest")

    # 3. Click SAVE to finish onboarding
    add_employee_page.click_save()

    # 4. Navigate to Admin module -> User Management -> Users
    add_employee_page.navigate_to_admin()

    # 5. Create a System User for the newly created employee
    system_users_page.click_add()
    add_user_page.enter_employee_name("FirstNameTest LastNameTest")

    add_user_page.select_user_role("Admin")
    add_user_page.select_status("Enabled")
    add_user_page.enter_username("testuser")
    add_user_page.enter_password("P@sswOrd123")
    add_user_page.enter_confirm_password("P@sswOrd123")

    add_user_page.click_save()
