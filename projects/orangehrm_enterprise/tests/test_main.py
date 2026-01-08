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

    def goto_login_page(self):
        self.navigate("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    def login(self, username, password):
        self.page.locator("[name='username']").fill(username)
        self.page.locator("[name='password']").fill(password)
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_url(re.compile("/web/index.php/dashboard.*", re.IGNORECASE), timeout=60000)

class PIMPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate_to_pim(self):
        self.page.locator("a[href*='/web/index.php/pim/viewPimModule']").click()
        self.page.wait_for_url(re.compile("/web/index.php/pim/viewPimModule", re.IGNORECASE), timeout=60000)

    def add_employee(self, first_name, last_name):
        self.page.get_by_role("button", name="Add").click()
        self.page.locator("[name='firstName']").fill(first_name)
        self.page.locator("[name='lastName']").fill(last_name)
        self.page.get_by_role("button", name="Save").click()
        self.page.wait_for_load_state("networkidle")

class AdminPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate_to_admin(self):
        self.page.locator("a[href*='/web/index.php/admin/viewAdminModule']").click()
        self.page.wait_for_url(re.compile("/web/index.php/admin/viewAdminModule", re.IGNORECASE), timeout=60000)

    def navigate_to_users(self):
        self.navigate_to_admin()
        self.page.locator("span.oxd-topbar-body-nav-tab-item").filter(has_text="User Management").click()
        self.page.get_by_role("menuitem", name="Users").click()
        self.page.wait_for_load_state("networkidle")

    def add_user(self, employee_name, username, password):
        self.page.get_by_role("button", name="Add").click()
        self.page.get_by_text("User Role").locator("xpath=//following::div[@class='oxd-select-text-input'][1]").click()
        self.page.get_by_role("option", name="Admin").click()
        self.page.locator("input[placeholder='Type for hints...']").fill(employee_name)
        self.page.locator("div[role='listbox'] span").click()
        self.page.get_by_text("Status").locator("xpath=//following::div[@class='oxd-select-text-input'][1]").click()
        self.page.get_by_role("option", name="Enabled").click()
        self.page.locator("div:nth-child(1) > div > div:nth-child(2) > input").fill(username)
        self.page.locator("div:nth-child(2) > div > div:nth-child(2) > input").fill(password)
        self.page.locator("div:nth-child(3) > div > div:nth-child(2) > input").fill(password)
        self.page.get_by_role("button", name="Save").click()
        self.page.wait_for_load_state("networkidle")

def test_autonomous_flow(browser: Browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    pim_page = PIMPage(page)
    admin_page = AdminPage(page)

    login_page.goto_login_page()
    login_page.login("Admin", "orangehrm123")

    pim_page.navigate_to_pim()
    pim_page.add_employee("FirstNameTest", "LastNameTest")

    admin_page.navigate_to_users()
    admin_page.add_user("FirstNameTest LastNameTest", "TestUser", "TestPassword123!")

    login_page.take_screenshot("final_screenshot", "orangehrm_enterprise")