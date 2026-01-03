import pytest
from playwright.sync_api import Page, expect

def test_auto_generated(page: Page):
    page.goto("https://testgrid.io/")