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


class GenericPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("https://teams.live.com/free")
        self.page.wait_for_load_state("networkidle")

    @property
    def download_teams_button(self):
        return self.page.get_by_role("link", name="Download Teams")

    @property
    def sign_in_button(self):
        return self.page.get_by_role("link", name="Sign in")

    @property
    def open_teams_in_browser_button(self):
        return self.page.get_by_role("button", name="Open Teams in your browser")

    @property
    def join_a_meeting_button(self):
        return self.page.get_by_role("button", name="Join a meeting")

    @property
    def teams_meetings_link(self):
        return self.page.get_by_text("Teams meetings")

    @property
    def need_help_link(self):
        return self.page.get_by_text("Need help?")


def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    generic_page = GenericPage(page)
    generic_page.goto()

    # 2. Logic (using POM)
    # Locate the buttons and links and assert visibility
    expect(generic_page.download_teams_button).to_be_visible()
    expect(generic_page.sign_in_button).to_be_visible()
    expect(generic_page.open_teams_in_browser_button).to_be_visible()
    expect(generic_page.join_a_meeting_button).to_be_visible()
    expect(generic_page.teams_meetings_link).to_be_visible()

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
    context.close()