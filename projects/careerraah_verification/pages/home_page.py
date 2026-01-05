"""
Page Object Model: HomePage
Represents: /
Auto-generated from exploration trace
"""
from playwright.sync_api import Page, expect


class HomePage:
    """Page Object for /"""
    
    def __init__(self, page: Page):
        self.page = page
        # Locators - defined once, reused everywhere
        
        
        self.careerraah_home_link = page.get_by_role("link", name="CareerRaah UPSKILL PLATFORM")  # a - CareerRaah Home
        
        

    def goto(self):
        """Navigate to HomePage"""
        self.page.goto("/")

    
    def click_careerraah_home_link(self):
        """
        Click careerraah home link
        
        
        """
        
        self.careerraah_home_link.click()  # Click careerraah_home_link
        
    
    