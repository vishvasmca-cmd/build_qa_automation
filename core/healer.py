import json
import os
import re
from playwright.sync_api import Page
from miner import extract_dom_snapshot, analyze_page
import asyncio

class Healer:
    """
    Self-healing engine for Playwright locators.
    """
    def __init__(self, llm):
        self.llm = llm

    def find_alternative(self, page: Page, failed_locator: str, context_goal: str):
        """
        Takes a failed locator and tries to find a replacement in the live DOM.
        """
        print(f"🔧 Attempting to heal failed locator: {failed_locator}")
        
        # 1. Capture fresh DOM
        # We need a sync version or use a helper
        # Since this runs in a sync test, we might need a sync wrapper for analyze_page
        # For simplicity in this demo, let's assume we can run a quick extraction
        
        return None # Placeholder for now, implemented in smart_action

def smart_action(page, primary_locator, action_type, value=None, goal=""):
    """
    Wraps Playwright actions with a retry/healing loop.
    """
    try:
        if action_type == 'click':
            page.locator(primary_locator).click(timeout=5000)
        elif action_type == 'fill':
            page.locator(primary_locator).fill(value, timeout=5000)
        return True
    except Exception as e:
        print(f"⚠️ Primary locator failed: {primary_locator}. Healing...")
        # 1. Find all potential candidates with data-test
        # (This is a simplified heuristic healer)
        all_elements = page.query_selector_all("[data-test], button, a")
        # Logic: If 'backpack' was in original, find 'backpack' in new
        keywords = re.findall(r'[\w-]+', primary_locator)
        
        for el in all_elements:
            attr = el.get_attribute("data-test") or el.inner_text().lower()
            if any(k in str(attr).lower() for k in keywords if len(k) > 3):
                try:
                    print(f"✨ Found potential match: {attr}. Retrying...")
                    if action_type == 'click': el.click()
                    else: el.fill(value)
                    return True
                except: continue
        
        raise e # If no healing worked, raise original
