"""
Smart Locator Module - Deterministic Element Finding

This module provides intelligent element location strategies that try
deterministic methods before falling back to expensive AI vision calls.

Goal: Reduce AI API calls by 50% (300 → 150 per test)
"""

from typing import Optional, Dict
from playwright.async_api import Page
import re


async def find_element_smart(page: Page, description: str) -> Optional[Dict]:
    """
    Try deterministic element finding strategies before AI fallback.
    
    Cascading strategy (stops at first unique match):
    1. data-testid / data-test attributes
    2. aria-label attributes
    3. placeholder attributes  
    4. name attributes
    5. Semantic label associations
    
    Args:
        page: Playwright Page object
        description: Human-readable element description (e.g., "Username", "Submit")
        
    Returns:
        {
            "selector": "css_selector",
            "confidence": 0.95,
            "method": "testid|aria-label|placeholder|name|label-assoc",
            "count": 1
        } if unique match found, None otherwise (triggers AI fallback)
    """
    
    # Normalize description for matching
    desc_lower = description.lower().strip()
    desc_clean = re.sub(r'[^a-z0-9\s]', '', desc_lower)  # Remove special chars
    
    # Strategy 1: data-testid / data-test (highest priority - explicit test hooks)
    for attr in ["data-testid", "data-test"]:
        # Try exact match first
        selector = f"[{attr}='{desc_clean}']"
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.98,
                "method": f"{attr}-exact",
                "count": 1
            }
        
        # Try partial match (contains)
        selector = f"[{attr}*='{desc_clean}']"
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.95,
                "method": f"{attr}-partial",
                "count": 1
            }
    
    # Strategy 2: aria-label (accessibility attributes)
    selector = f"[aria-label*='{description}' i]"  # Case-insensitive
    count = await page.locator(selector).count()
    if count == 1:
        return {
            "selector": selector,
            "confidence": 0.92,
            "method": "aria-label",
            "count": 1
        }
    
    # Strategy 3: placeholder (input field hints)
    selector = f"[placeholder*='{description}' i]"
    count = await page.locator(selector).count()
    if count == 1:
        return {
            "selector": selector,
            "confidence": 0.90,
            "method": "placeholder",
            "count": 1
        }
    
    # Strategy 4: name attribute (form field names)
    selector = f"[name*='{desc_clean}']"
    count = await page.locator(selector).count()
    if count == 1:
        return {
            "selector": selector,
            "confidence": 0.88,
            "method": "name",
            "count": 1
        }
    
    # Strategy 5: id attribute (element IDs)
    selector = f"[id*='{desc_clean}']"
    count = await page.locator(selector).count()
    if count == 1:
        return {
            "selector": selector,
            "confidence": 0.85,
            "method": "id",
            "count": 1
        }
    
    # Strategy 6: Semantic label + input association
    # This finds inputs associated with labels containing the description
    try:
        # Method A: label wrapping input
        selector = f"label:has-text('{description}') input"
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.87,
                "method": "label-wrapped",
                "count": 1
            }
        
        # Method B: label with for= attribute
        # Find label text, get its for attribute, find input with that id
        labels = page.locator(f"label:has-text('{description}')")
        label_count = await labels.count()
        if label_count == 1:
            for_attr = await labels.get_attribute("for")
            if for_attr:
                input_selector = f"#{for_attr}"
                input_count = await page.locator(input_selector).count()
                if input_count == 1:
                    return {
                        "selector": input_selector,
                        "confidence": 0.87,
                        "method": "label-for",
                        "count": 1
                    }
    except Exception:
        pass  # Label association failed, continue
    
    # Strategy 7: Button/link text (exact text match)
    for tag in ["button", "a"]:
        # Exact text match
        selector = f"{tag}:has-text('{description}')"
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.90,
                "method": f"{tag}-text-exact",
                "count": 1
            }
    
    # All deterministic strategies failed - return None to trigger AI fallback
    return None
