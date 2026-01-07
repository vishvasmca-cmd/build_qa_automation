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

    def goto(self):
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.page.wait_for_load_state("networkidle")

    @property
    def forgot_password_link(self):
        return self.page.get_by_text("Forgot your password?")

    @property
<<<<<<< Updated upstream
    def orangehrm_inc_link(self):
        return self.page.get_by_role("link", name="OrangeHRM, Inc")

    @property
    def social_media_icon(self):
=======
    def social_media_icon_link(self):
>>>>>>> Stashed changes
        return self.page.locator("xpath=//*[@id=\"app\"]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/a[1]")

    def click_forgot_password(self):
        self.forgot_password_link.click()

<<<<<<< Updated upstream
    def click_orangehrm_inc_link(self):
        self.orangehrm_inc_link.click()

    def click_social_media_icon(self):
        self.social_media_icon.click()
=======
    def click_social_media_icon_link(self):
        self.social_media_icon_link.click()
>>>>>>> Stashed changes

class OrangehrmResetPasswordPage:
    def __init__(self, page):
        self.page = page

    @property
    def username_field(self):
        return self.page.locator("[name='username']")

    @property
    def reset_password_button(self):
        return self.page.get_by_role("button", name="Reset Password")

    def fill_username(self, username):
        self.username_field.fill(username)

    def click_reset_password(self):
        self.reset_password_button.click()

class PasswordResetConfirmationPage:
    def __init__(self, page):
        self.page = page

    @property
    def orangehrm_inc_link(self):
        return self.page.get_by_role("link", name="OrangeHRM, Inc")

    def click_orangehrm_inc_link(self):
        self.orangehrm_inc_link.click()

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    login_page = OrangehrmLoginPage(page)
    reset_password_page = OrangehrmResetPasswordPage(page)
    password_reset_confirmation_page = PasswordResetConfirmationPage(page)

<<<<<<< Updated upstream
    # Step 0: Click 'Forgot your password?' link
    login_page.click_forgot_password_link()
    page.wait_for_load_state("networkidle")

    # Step 1: Fill username on the reset password page
    reset_password_page.fill_username("testuser")

    # Step 2: Click 'Reset Password' button
    reset_password_page.click_reset_password_button()
    page.wait_for_load_state("networkidle")

    # Assert that the reset password link was sent successfully
    expect(page.locator('body')).to_have_text("Reset Password link sent successfully", timeout=15000)

    # Step 3: Click OrangeHRM, Inc link to return to the login page
    # password_reset_confirmation_page.click_orangehrm_inc_link()
    # page.wait_for_load_state("networkidle")

    # Step 4: Click social media icon
    # login_page.click_social_media_icon()
=======
    login_page.goto()

    # Step 0: Click 'Forgot your password?' link
    login_page.click_forgot_password()

    # Step 2: Fill username on reset password page
    reset_password_page.fill_username("testuser")

    # Step 3: Click 'Reset Password' button
    reset_password_page.click_reset_password()

    # Step 5: Click 'OrangeHRM, Inc' link on confirmation page
    password_reset_confirmation_page.click_orangehrm_inc_link()

    # Step 8, 9, 10: Click social media icon link
    login_page.click_social_media_icon_link()
>>>>>>> Stashed changes

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()
