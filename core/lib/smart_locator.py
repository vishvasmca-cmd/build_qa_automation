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
    
    # === ADVANCED STRATEGIES FOR LEGACY SITES ===
    
    # Strategy 8: Fuzzy Token Matching (for "First Name" → "firstname", "first_name")
    desc_tokens = desc_clean.split()
    if len(desc_tokens) >= 2:  # Multi-word descriptions
        for tag in ["input", "select", "textarea"]:
            for token in desc_tokens:
                if len(token) >= 3:  # Skip short words
                    # Match token in name/id/class
                    selector = f"{tag}[name*='{token}' i], {tag}[id*='{token}' i], {tag}[class*='{token}' i]"
                    count = await page.locator(selector).count()
                    if count == 1:
                        return {
                            "selector": selector,
                            "confidence": 0.75,
                            "method": "fuzzy-token",
                            "count": 1
                        }
    
    # Strategy 9: Proximity-Based (text label → next input)
    try:
        # Find visible text containing description
        text_selector = f"text={description}"
        text_count = await page.locator(text_selector).count()
        if text_count == 1:
            # Try sibling selectors
            for proximity_selector in [
                f"text={description} + input",  # Immediate next sibling
                f"text={description} ~ input",  # Any following sibling
                f"text={description} >> xpath=.. >> input",  # Parent's input
            ]:
                count = await page.locator(proximity_selector).count()
                if count == 1:
                    return {
                        "selector": proximity_selector,
                        "confidence": 0.80,
                        "method": "proximity",
                        "count": 1
                    }
    except Exception:
        pass
    
    # Strategy 10: Case-Insensitive Text Variations
    # For buttons like "SUBMIT", "Submit", "submit"
    for tag in ["button", "a", "span"]:
        selector = f"{tag}:text-is('{description}')"  # Exact case-insensitive
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.85,
                "method": "text-case-insensitive",
                "count": 1
            }
    
    # Strategy 11: Visual Scoring Fallback (when count > 1, pick most prominent)
    # Try common patterns that might have multiple matches
    fallback_selectors = [
        f"[placeholder*='{description}' i]",
        f"[aria-label*='{description}' i]",
        f"button:has-text('{description}')",
        f"input[name*='{desc_clean}']",
        f"[id*='{desc_clean}']",
    ]
    
    for selector in fallback_selectors:
        count = await page.locator(selector).count()
        if count > 1:
            # Use visual scoring to pick best element
            best_selector = await _visual_scoring_fallback(page, selector)
            if best_selector:
                return {
                    "selector": best_selector,
                    "confidence": 0.70,  # Lower confidence (position-based)
                    "method": "visual-scoring",
                    "count": 1
                }
    
    # All deterministic strategies failed - return None to trigger AI fallback
    return None


async def _visual_scoring_fallback(page: Page, selector: str) -> Optional[str]:
    """
    When multiple elements match, pick the most visually prominent one.
    
    Scores based on:
    - Centrality (closer to screen center)
    - Size (larger elements)
    - Visibility (fully visible)
    
    Returns: nth-based selector for best element, or None if all hidden
    """
    try:
        locator = page.locator(selector)
        count = await locator.count()
        
        if count <= 1:
            return selector  # Already unique
        
        viewport = page.viewport_size or {"width": 1280, "height": 720}
        center_x, center_y = viewport["width"] / 2, viewport["height"] / 2
        
        scores = []
        for i in range(count):
            el = locator.nth(i)
            
            # Check visibility first
            is_visible = await el.is_visible()
            if not is_visible:
                scores.append(-1)  # Penalize hidden elements
                continue
            
            # Get bounding box
            box = await el.bounding_box()
            if not box:
                scores.append(0)
                continue
            
            # Calculate element center
            el_center_x = box['x'] + box['width'] / 2
            el_center_y = box['y'] + box['height'] / 2
            
            # 1. Centrality score (inverse distance from screen center)
            distance = ((el_center_x - center_x)**2 + (el_center_y - center_y)**2)**0.5
            centrality = 1000 - min(distance, 1000)  # Cap at 1000
            
            # 2. Size score
            area = box['width'] * box['height']
            size_score = min(area * 0.1, 500)  # Cap contribution
            
            # 3. Visibility bonus
            visibility_bonus = 1000
            
            total_score = centrality + size_score + visibility_bonus
            scores.append(total_score)
        
        # Find highest scoring element
        if not scores or max(scores) <= 0:
            return None  # All hidden
        
        best_idx = scores.index(max(scores))
        return f"{selector} >> nth={best_idx}"
        
    except Exception:
        return None

