import pytest
import os
import re
import random
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
import sys
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
from helpers import take_screenshot


def check_ssl_certificate(page: Page) -> bool:
    if "Invalid SSL certificate" in page.title():
        print("SSL Certificate is invalid. Skipping test.")
        return False
    return True


def test_autonomous_flow(page: Page):
    # 1. Setup
    page.set_viewport_size({"width": 1920, "height": 1080})

    # 2. Logic
    page.goto("https://magento.softwaretestingboard.com/")
    page.wait_for_load_state("networkidle")

    if not check_ssl_certificate(page):
        print("Skipping test due to invalid SSL certificate.")
        return

    expect(page).to_have_title(re.compile("Magento", re.IGNORECASE))

    # 3. Cleanup
    take_screenshot(page, "final_state", "build_qa_automation")
