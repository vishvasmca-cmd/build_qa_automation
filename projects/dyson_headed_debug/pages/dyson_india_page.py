import re
from playwright.sync_api import Page, expect
from .base_page import BasePage

class DysonIndiaPage(BasePage):
    """
    Dyson India Home / Navigation Page Object.
    """
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_deals(self):
        self.page.get_by_role("link", name="Deals").first.click()

    def navigate_to_vacuum_wet_cleaners(self):
        self.page.get_by_role("link", name="Vacuum & wet cleaners").first.click()

    def navigate_to_hair_care(self):
        self.page.get_by_role("link", name="Hair care").first.click()

    def navigate_to_air_purifier(self):
        # On some Dyson layouts, it might be "Air purifier" or "Air treatment"
        # We try to be flexible
        self.page.get_by_role("link", name=re.compile("Air purifier|Air treatment", re.I)).first.click()

    def navigate_to_headphones(self):
        self.page.get_by_role("link", name="Headphones").first.click()

    def navigate_to_lighting(self):
        self.page.get_by_role("link", name="Lighting").first.click()

    def navigate_to_support(self):
        self.page.get_by_role("link", name="Support").first.click()