"""
Page Object Model: DocsIntroPage
Represents: /docs/intro
Auto-generated from exploration trace
"""
from playwright.sync_api import Page, expect


class DocsIntroPage:
    """Page Object for /docs/intro"""
    
    def __init__(self, page: Page):
        self.page = page
        # Locators - defined once, reused everywhere
        
        
        self.get_started_link = page.get_by_role("link", name="GET STARTED")  # a - GET STARTED
        
        

    def goto(self):
        """Navigate to DocsIntroPage"""
        self.page.goto("/docs/intro")

    
    def click_get_started_link(self):
        """
        Click get started link
        
        
        """
        
        self.get_started_link.click()  # Click get_started_link
        
    
    