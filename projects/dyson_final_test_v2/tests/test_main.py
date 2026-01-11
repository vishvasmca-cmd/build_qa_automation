# Auto-generated Test
import pytest
import os
import re
from playwright.sync_api import Page, Browser, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("https://www.dyson.in/")

    def click_deals_link(self):
        self.page.get_by_role("link", name=re.compile("Deals", re.IGNORECASE)).first.click()
        self.page.wait_for_url("**/deals/**")

    def click_vacuum_wet_cleaners_link(self):
        self.page.get_by_role("link", name=re.compile("Vacuum & wet cleaners", re.IGNORECASE)).first.click()
        self.page.wait_for_url("**/vacuum-wet-cleaners/**")

    def click_hair_care_link(self):
        self.page.get_by_role("link", name=re.compile("Hair care", re.IGNORECASE)).first.click()
        self.page.wait_for_url("**/hair-care/**")

    def click_air_purifier_link(self):
        self.page.get_by_role("link", name=re.compile("Air purifier", re.IGNORECASE)).first.click()
        self.page.wait_for_url("**/air-treatment/**")

    def click_headphones_link(self):
        self.page.get_by_role("link", name=re.compile("Headphones", re.IGNORECASE)).first.click()
        self.page.wait_for_url("**/headphones/**")

    def click_lighting_link(self):
        self.page.get_by_role("link", name=re.compile("Lighting", re.IGNORECASE)).first.click()
        self.page.wait_for_url("**/lighting/**")

    def click_support_link(self):
        self.page.get_by_role("link", name=re.compile("Support", re.IGNORECASE)).first.click()
        self.page.wait_for_url("**/support/**")

def take_screenshot(page: Page, filename: str, folder: str = 'screenshots'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    page.screenshot(path=f"{folder}/{filename}.png")

@pytest.mark.skipif(not os.environ.get("TAKE_SCREENSHOTS"), reason="Screenshots are disabled")
def test_autonomous_flow(page: Page):
    # page = browser.new_page()  <-- Removed, use fixture
    home_page = HomePage(page)

    home_page.navigate()
    expect(page).to_have_url("https://www.dyson.in/")
    take_screenshot(page, 'home_page', 'dyson')

    home_page.click_deals_link()
    expect(page).to_have_url(re.compile("deals"))
    take_screenshot(page, 'deals_page', 'dyson')

    home_page.click_vacuum_wet_cleaners_link()
    expect(page).to_have_url(re.compile("vacuum-wet-cleaners"))
    take_screenshot(page, 'vacuum_page', 'dyson')

    home_page.click_hair_care_link()
    expect(page).to_have_url(re.compile("hair-care"))
    take_screenshot(page, 'hair_care_page', 'dyson')

    home_page.click_air_purifier_link()
    expect(page).to_have_url(re.compile("air-treatment"))
    take_screenshot(page, 'air_purifier_page', 'dyson')

    home_page.click_headphones_link()
    expect(page).to_have_url(re.compile("headphones"))
    take_screenshot(page, 'headphones_page', 'dyson')

    home_page.click_lighting_link()
    expect(page).to_have_url(re.compile("lighting"))
    take_screenshot(page, 'lighting_page', 'dyson')

    home_page.click_support_link()
    expect(page).to_have_url(re.compile("support"))
    take_screenshot(page, 'support_page', 'dyson')

    page.close()