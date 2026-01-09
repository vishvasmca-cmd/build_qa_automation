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
        self.login_button_locator = "page.get_by_role(\"button\", name=\"Login\")"

    def login(self, username, password):
        self.page.locator(self.username_locator).fill(username)
        self.page.locator(self.password_locator).fill(password)
        self.page.locator(eval(self.login_button_locator)).click()
        self.page.wait_for_load_state("networkidle")

class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_link_locator = "page.get_by_role(\"link\", name=\"PIM\")"

    def navigate_to_pim(self):
        self.page.locator(eval(self.pim_link_locator)).click()
        self.page.wait_for_load_state("networkidle")

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = "page.get_by_role(\"button\", name=\"Add\")"

    def navigate_to_add_employee(self):
        self.page.locator(eval(self.add_button_locator)).click()
        self.page.wait_for_load_state("networkidle")

class AddEmployeeOrangehrmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_locator = "[name='firstName']"
        self.last_name_locator = "[name='lastName']"
        self.save_button_locator = "page.get_by_role(\"button\", name=\"Save\")"

    def add_employee(self, first_name, last_name):
        self.page.locator(self.first_name_locator).fill(first_name)
        self.page.locator(self.last_name_locator).fill(last_name)
        self.page.locator(eval(self.save_button_locator)).click()
        self.page.wait_for_load_state("networkidle")

class OrangehrmPimPersonalDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.admin_link_locator = "page.get_by_role(\"link\", name=\"Admin\")"

    def navigate_to_admin(self):
        self.page.locator(eval(self.admin_link_locator)).click()
        self.page.wait_for_load_state("networkidle")

class SystemUsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = "page.get_by_role(\"button\", name=\"Add\")"

    def navigate_to_add_user(self):
        self.page.locator(eval(self.add_button_locator)).click()
        self.page.wait_for_load_state("networkidle")

class AddUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.employee_name_locator = "page.get_by_placeholder(\"Type for hints...\")"
        self.save_button_locator = "page.get_by_role(\"button\", name=\"Save\")"
        self.cancel_button_locator = "page.get_by_role(\"button\", name=\"Cancel\")"

    def fill_employee_name(self, employee_name):
        self.page.locator(eval(self.employee_name_locator)).fill(employee_name)

    def save_user(self):
        self.page.locator(eval(self.save_button_locator)).click()
        self.page.wait_for_load_state("networkidle")

    def cancel_add_user(self):
        self.page.locator(eval(self.cancel_button_locator)).click()
        self.page.wait_for_load_state("networkidle")

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeeOrangehrmPage(page)
    system_users_page = SystemUsersPage(page)
    add_user_page = AddUserPage(page)
    pim_personal_details_page = OrangehrmPimPersonalDetailsPage(page)

    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.login("Admin", "admin123")

    dashboard_page.navigate_to_pim()
    employee_list_page.navigate_to_add_employee()
    add_employee_page.add_employee("FirstNameTest", "LastNameTest")

    pim_personal_details_page.navigate_to_admin()
    system_users_page.navigate_to_add_user()

    # The trace doesn't provide the employee name to fill, so I'm adding a placeholder
    add_user_page.fill_employee_name("Type for hints...")
    add_user_page.save_user()

    # The trace shows that the save action failed, so we cancel and try again
    add_user_page.cancel_add_user()
    system_users_page.navigate_to_add_user()
    # The trace doesn't provide the employee name to fill, so I'm adding a placeholder
    add_user_page.fill_employee_name("Type for hints...")
    add_user_page.save_user()