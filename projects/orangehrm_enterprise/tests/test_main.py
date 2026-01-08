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
        self.login_button_locator = "button[type='submit']"

    def enter_username(self, username):
        self.page.locator(self.username_locator).fill(username)

    def enter_password(self, password):
        self.page.locator(self.password_locator).fill(password)

    def click_login(self):
        self.page.locator(self.login_button_locator).click()

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_link_locator = "a[href='/web/index.php/pim/viewPimModule']"

    def navigate_to_pim(self):
        self.page.locator(self.pim_link_locator).click()

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = self.page.get_by_role("button", name="Add")

    def click_add(self):
        self.add_button_locator.click()

class AddEmployeeOrangehrmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_locator = "[name='firstName']"
        self.last_name_locator = "[name='lastName']"
        self.save_button_locator = self.page.get_by_role("button", name="Save")

    def enter_first_name(self, first_name):
        self.page.locator(self.first_name_locator).fill(first_name)

    def enter_last_name(self, last_name):
        self.page.locator(self.last_name_locator).fill(last_name)

    def click_save(self):
        self.save_button_locator.click()

class OrangehrmPimPersonalDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.admin_link_locator = self.page.get_by_role("link", name="Admin")

    def navigate_to_admin(self):
        self.admin_link_locator.click()

class AdminUserManagementPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = self.page.get_by_role("button", name="Add")

    def click_add(self):
        self.add_button_locator.click()

class GenericPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

import re
from playwright.sync_api import Browser, Page, expect


# from core.utils import take_screenshot # ALREADY PRE-IMPORTED. DO NOT IMPORT IT

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name: str, project_name: str):
        take_screenshot(self.page, name, project_name)


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_locator = "[name='username']"
        self.password_locator = "[name='password']"
        self.login_button_locator = "button[type='submit']"

    def enter_username(self, username: str):
        self.page.locator(self.username_locator).fill(username)

    def enter_password(self, password: str):
        self.page.locator(self.password_locator).fill(password)

    def click_login(self):
        self.page.locator(self.login_button_locator).click()


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.pim_link_locator = self.page.get_by_role("link", name="PIM")

    def navigate_to_pim(self):
        self.pim_link_locator.click()


class EmployeeListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button_locator = self.page.get_by_role("button", name="Add")

    def click_add(self):
        self.add_button_locator.click()


class AddEmployeeOrangehrmPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_locator = "[name='firstName']"
        self.last_name_locator = "[name='lastName']"
        self.save_button_locator = self.page.get_by_role("button", name="Save")

    def enter_first_name(self, first_name: str):
        self.page.locator(self.first_name_locator).fill(first_name)

    def enter_last_name(self, last_name: str):
        self.page.locator(self.last_name_locator).fill(last_name)

    def click_save(self):
        self.save_button_locator.click()


class OrangehrmPimPersonalDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.admin_link_locator = self.page.get_by_role("link", name="Admin")

    def navigate_to_admin(self):
        self.admin_link_locator.click()


class AdminUserManagementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button_locator = self.page.get_by_role("button", name="Add")

    def click_add(self):
        self.add_button_locator.click()


class GenericPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)


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
    expect(page).to_have_url(re.compile(".*/auth/login.*", re.IGNORECASE))

    login_page.enter_username("Admin")
    login_page.enter_password("admin123")
    login_page.click_login()

    expect(page).to_have_url(re.compile(".*/dashboard.*", re.IGNORECASE))

    dashboard_page.navigate_to_pim()
    expect(page).to_have_url(re.compile(".*/pim/viewEmployeeList.*", re.IGNORECASE))

    employee_list_page.click_add()
    expect(page).to_have_url(re.compile(".*/pim/addEmployee.*", re.IGNORECASE))

    add_employee_page.enter_first_name("FirstNameTest")
    add_employee_page.enter_last_name("LastNameTest")
    add_employee_page.click_save()

    expect(page).to_have_url(re.compile(".*/viewPersonalDetails/empNumber/.*", re.IGNORECASE))

    pim_personal_details_page.navigate_to_admin()
    expect(page).to_have_url(re.compile(".*/admin/viewSystemUsers.*", re.IGNORECASE))

    admin_user_management_page.click_add()
    expect(page).to_have_url(re.compile(".*/admin/saveSystemUser.*", re.IGNORECASE))