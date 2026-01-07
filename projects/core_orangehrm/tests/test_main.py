# Auto-generated Test
import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
from helpers import take_screenshot


class OrangehrmLoginPage:
    def __init__(self, page):
        self.page = page

    @property
    def forgot_password_link(self):
        return self.page.get_by_text("Forgot your password?")

    def click_forgot_password_link(self):
        self.forgot_password_link.click()

    def goto(self):
        self.page.goto("https://opensource-demo.orangehrmlive.com/")
        self.page.wait_for_load_state("networkidle")

class OrangehrmResetPasswordPage:
    def __init__(self, page):
        self.page = page

    @property
    def username_input(self):
        return self.page.locator("[name='username']")

    @property
    def reset_password_button(self):
        return self.page.get_by_role("button", name="Reset Password")

    @property
    def orangehrm_inc_link(self):
        return self.page.get_by_role("link", name="OrangeHRM, Inc")

    def fill_username(self, username):
        self.username_input.fill(username)

    def click_reset_password_button(self):
        self.reset_password_button.click()

    def click_orangehrm_inc_link(self):
        self.orangehrm_inc_link.click()

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    login_page = OrangehrmLoginPage(page)
    reset_password_page = OrangehrmResetPasswordPage(page)

    # Step 0: Click the 'Forgot your password?' link
    login_page.click_forgot_password_link()

    # Step 6: Fill username on reset password page
    reset_password_page.fill_username("Admin")

    # Step 4: Click reset password button
    reset_password_page.click_reset_password_button()

    # Step 7: Click OrangeHRM, Inc link
    reset_password_page.click_orangehrm_inc_link()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()