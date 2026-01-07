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

    @property
    def orangehrm_inc_link(self):
        return self.page.get_by_role("link", name="OrangeHRM, Inc")

    def click_orangehrm_inc_link(self):
        self.orangehrm_inc_link.click()

    @property
    def social_media_link(self):
        return self.page.locator("xpath=//*[@id=\"app\"]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/a[1]")

    def click_social_media_link(self):
        self.social_media_link.click()


class OrangehrmResetPasswordPage:
    def __init__(self, page):
        self.page = page

    @property
    def username_field(self):
        return self.page.locator("[name='username']")

    def fill_username(self, username):
        self.username_field.fill(username)

    @property
    def reset_password_button(self):
        return self.page.get_by_role("button", name="Reset Password")

    def click_reset_password_button(self):
        self.reset_password_button.click()


class PasswordResetConfirmationPage:
    def __init__(self, page):
        self.page = page

    @property
    def orangehrm_inc_link(self):
        return self.page.get_by_role("link", name="OrangeHRM, Inc")

    def click_orangehrm_inc_link(self):
        self.orangehrm_inc_link.click()


class LoginPage:
    def __init__(self, page):
        self.page = page

    @property
    def orangehrm_inc_link(self):
        return self.page.get_by_role("link", name="OrangeHRM, Inc")

    def navigate_to_homepage(self):
        self.page.goto("https://opensource-demo.orangehrmlive.com/")


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    login_page = OrangehrmLoginPage(page)
    reset_password_page = OrangehrmResetPasswordPage(page)
    password_reset_confirmation_page = PasswordResetConfirmationPage(page)
    base_login_page = LoginPage(page)

    # Step 0: Click 'Forgot your password?' link
    login_page.click_forgot_password_link()

    # Step 1: Navigate back to login page
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Step 2: Fill username on reset password page
    reset_password_page.fill_username("Admin")

    # Step 3: Click Reset Password button
    reset_password_page.click_reset_password_button()

    # Step 4: Navigate back to login page
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Step 5: Click OrangeHRM, Inc link on PasswordResetConfirmationPage
    password_reset_confirmation_page.click_orangehrm_inc_link()

    # Step 6: Navigate to homepage
    base_login_page.navigate_to_homepage()

    # Step 7: Scroll (removed as it's not reliable and auto-scrolling should handle it)

    # Step 8: Click social media link
    login_page.click_social_media_link()

    # Step 9: Click social media link again
    login_page.click_social_media_link()

    # Step 10: Click social media link again
    login_page.click_social_media_link()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()