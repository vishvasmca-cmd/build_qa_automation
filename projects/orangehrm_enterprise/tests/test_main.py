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

from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_locator = "[name='username']"
        self.password_locator = "[name='password']"
        self.login_button_locator = "text=Login"

    def login(self, username, password):
        self.page.locator(self.username_locator).fill(username)
        self.page.locator(self.password_locator).fill(password)
        self.page.locator(self.login_button_locator).first.click()

from .base_page import BasePage

class OrangehrmDashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pim_link_locator = "text=PIM"

    def navigate_to_pim(self):
        self.page.locator(self.pim_link_locator).click()

from .base_page import BasePage

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button_locator = "button:has-text('Add')"

    def navigate_to_add_employee(self):
        self.page.locator(self.add_button_locator).click()

from .base_page import BasePage

class OrangehrmAddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_locator = "[name='firstName']"
        self.last_name_locator = "[name='lastName']"
        self.save_button_locator = "button:has-text('Save')"

    def add_employee(self, first_name, last_name):
        self.page.locator(self.first_name_locator).fill(first_name)
        self.page.locator(self.last_name_locator).fill(last_name)
        self.page.locator(self.save_button_locator).click()

from playwright.sync_api import Browser
from projects.orangehrm_enterprise.pages.login_page import LoginPage
from projects.orangehrm_enterprise.pages.dashboard_page import OrangehrmDashboardPage
from projects.orangehrm_enterprise.pages.employee_list_page import EmployeeListPage
from projects.orangehrm_enterprise.pages.add_employee_page import OrangehrmAddEmployeePage
from projects.orangehrm_enterprise.pages.base_page import BasePage


def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    dashboard_page = OrangehrmDashboardPage(page)
    employee_list_page = EmployeeListPage(page)
    add_employee_page = OrangehrmAddEmployeePage(page)

    login_page.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.login("Admin", "admin123")
    dashboard_page.navigate_to_pim()
    employee_list_page.navigate_to_add_employee()
    add_employee_page.add_employee("FirstNameTest", "LastNameTest")
    take_screenshot(page, "add_employee_success", "orangehrm_enterprise")
    page.close()