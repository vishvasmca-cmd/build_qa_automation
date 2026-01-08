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

from playwright.sync_api import Page


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.username_locator = "[name='username']"
        self.password_locator = "[name='password']"
        self.login_button_locator = "page.get_by_role(\"button\", name=\"Login\")"

    def enter_username(self, username):
        self.page.locator(self.username_locator).fill(username)

    def enter_password(self, password):
        self.page.locator(self.password_locator).fill(password)

    def click_login(self):
        self.page.locator(self.login_button_locator).click()

from playwright.sync_api import Page


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.pim_link_locator = "page.get_by_role(\"link\", name=\"PIM\")"

    def click_pim_link(self):
        self.page.locator(self.pim_link_locator).click()

from playwright.sync_api import Page


class EmployeeListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.add_button_locator = "page.get_by_role(\"button\", name=\"Add\")"

    def click_add_button(self):
        self.page.locator(self.add_button_locator).click()

from playwright.sync_api import Page


class AddEmployeeOrangehrmPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.first_name_locator = "[name='firstName']"
        self.last_name_locator = "[name='lastName']"
        self.save_button_locator = "page.get_by_role(\"button\", name=\"Save\")"

    def enter_first_name(self, first_name):
        self.page.locator(self.first_name_locator).fill(first_name)

    def enter_last_name(self, last_name):
        self.page.locator(self.last_name_locator).fill(last_name)

    def click_save_button(self):
        self.page.locator(self.save_button_locator).click()

from playwright.sync_api import Page


class OrangehrmPimPersonalDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.admin_link_locator = "page.get_by_role(\"link\", name=\"Admin\")"

    def click_admin_link(self):
        self.page.locator(self.admin_link_locator).click()

from playwright.sync_api import Page


class AdminUserManagementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.add_button_locator = "page.get_by_role(\"button\", name=\"Add\")"

    def click_add_button(self):
        self.page.locator(self.add_button_locator).click()

from playwright.sync_api import Page


class GenericPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

from playwright.sync_api import Browser, expect
import re


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = AddEmployeeOrangehrmPage(page)
    pim_personal_details_page = OrangehrmPimPersonalDetailsPage(page)
    admin_user_management_page = AdminUserManagementPage(page)
    generic_page = GenericPage(page)

    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    expect(page).to_have_url(re.compile(".*/auth/login.*"))

    login_page.enter_username("Admin")
    login_page.enter_password("admin123")
    login_page.click_login()

    expect(page).to_have_url(re.compile(".*/dashboard.*"))

    dashboard_page.click_pim_link()
    expect(page).to_have_url(re.compile(".*/pim/viewEmployeeList.*"))

    employee_list_page.click_add_button()
    expect(page).to_have_url(re.compile(".*/pim/addEmployee.*"))

    add_employee_page.enter_first_name("FirstNameTest")
    add_employee_page.enter_last_name("LastNameTest")
    add_employee_page.click_save_button()

    expect(page).to_have_url(re.compile(".*/viewPersonalDetails/empNumber/.*"))

    pim_personal_details_page.click_admin_link()
    expect(page).to_have_url(re.compile(".*/admin/viewSystemUsers.*"))

    admin_user_management_page.click_add_button()
    expect(page).to_have_url(re.compile(".*/admin/saveSystemUser.*"))