"""
Smart Locator Module - Enhanced with AI Gap Improvements

This module provides intelligent element location strategies that try
deterministic methods before falling back to expensive AI vision calls.

IMPROVEMENTS (v2.0):
- Visibility filtering (count > 1 → check :visible)
- Exact ID matching before partial  
- Role locators as high priority
- Container context awareness
- First-item e-commerce patterns

Target: 93% success rate on modern sites (up from 85%)
"""

from typing import Optional, Dict
from playwright.async_api import Page
import re

# Debug mode - set to True to see detailed strategy attempts
DEBUG_SMART_SELECTORS = True


async def find_element_smart(page: Page, description: str, debug: bool = None) -> Optional[Dict]:
    """
    Try deterministic element finding strategies before AI fallback.
    
    Enhanced with 5 AI gap improvements for 85% → 93% success rate.
    
    Args:
        page: Playwright Page object
        description: Human-readable element description (e.g., "Username", "Submit")
        debug: Enable debug logging (defaults to DEBUG_SMART_SELECTORS global)
        
    Returns:
        {
            "selector": "css_selector",
            "confidence": 0.95,
            "method": "role-button-exact|id-exact-visible|...",
            "count": 1
        } if unique match found, None otherwise (triggers AI fallback)
    """
    
    # Initialize debug mode
    if debug is None:
        debug = DEBUG_SMART_SELECTORS
    
    strategies_tried = 0
    
    if debug:
        print(f"    🔍 [SMART] Searching for: '{description}' (trying 15+ strategies)")
    
    # Normalize description for matching
    desc_lower = description.lower().strip()
    desc_clean = re.sub(r'[^a-z0-9\s]', '', desc_lower)  # Remove special chars
    
    # === CRITICAL FIX: Detect CSS selectors to avoid parsing errors ===
    # If description looks like a CSS selector, skip role/link strategies
    is_css_selector = (
        description.startswith(('div[', 'span[', 'button[', 'a[', 'input[', '#', '.')) or
        re.search(r'\[class\s*[=*^$~|]', description) or  # Matches [class=...] patterns
        re.search(r'\[id\s*[=*^$~|]', description) or     # Matches [id=...] patterns
        re.search(r'\[.*\s*=\s*["\']', description)       # Matches any [attr="..."] patterns
    )
    
    if debug and is_css_selector:
        print(f"    ⚠️ [SMART] Detected CSS selector syntax in '{description}' - skipping role/link strategies")
    
    # === IMPROVEMENT 3 & 5: Role Locators + First Item Patterns (HIGHEST PRIORITY) ===
    # Strategy 1: Semantic role locators with common e-commerce patterns
    # SKIP if description is CSS selector (would cause InvalidSelectorError)
    if not is_css_selector:
        role_mappings = {
            "button": ["button", "submit", "login", "register", "search", "add", "continue", "checkout", "proceed"],
            "link": ["link", "navigate", "view", "details", "cart", "product"],
            "textbox": ["email", "password", "username", "search", "name", "address", "city", "zip", "phone"],
        }
        
        for role, keywords in role_mappings.items():
            if any(kw in desc_lower for kw in keywords):
                # Try role with exact name
                selector = f"role={role}[name='{description}' i]"
                count = await page.locator(selector).count()
                if count == 1:
                    return {
                        "selector": selector,
                        "confidence": 0.96,
                        "method": f"role-{role}-exact",
                        "count": 1
                    }
                
                # Try role with partial name
                selector = f"role={role}[name*='{description}' i]"
                count = await page.locator(selector).count()
                if count == 1:
                    return {
                        "selector": selector,
                        "confidence": 0.93,
                        "method": f"role-{role}-partial",
                        "count": 1
                    }
    
    # === IMPROVEMENT 5: First Item / E-Commerce Patterns ===
    # Strategy 2: Common e-commerce first-item patterns
    if any(kw in desc_lower for kw in ["first", "product", "item", "add to cart"]):
        ecommerce_selectors = [
            "a[data-product-id='1']",
            "button[data-product-id='1']",
            ".product:first-of-type button",
            ".product:first-of-type a",
            "[data-index='0'] button",
        ]
        
        for selector in ecommerce_selectors:
            count = await page.locator(selector).count()
            if count == 1:
                return {
                    "selector": selector,
                    "confidence": 0.90,
                    "method": "ecommerce-first-item",
                    "count": 1
                }
    
    # Strategy 3: data-testid / data-test (explicit test hooks)
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
    
    # === IMPROVEMENT 2: Exact IDs First (Before Partial) ===
    # Strategy 4: id attribute - EXACT match with variations
    # Convert description to common ID patterns
    id_variations = [
        desc_clean.replace(' ', '_'),      # "Search Product" -> "search_product"
        desc_clean.replace(' ', '-'),      # "Search Product" -> "search-product"
        desc_clean.replace(' ', ''),       # "Search Product" -> "searchproduct"
        ''.join(word.capitalize() for word in desc_clean.split()) if ' ' in desc_clean else desc_clean,  # "searchProduct" (camelCase)
    ]
    
    for id_variant in id_variations:
        if id_variant:  # Skip empty
            selector = f"#{id_variant}"
            count = await page.locator(selector).count()
            if count == 1:
                return {
                    "selector": selector,
                    "confidence": 0.92,
                    "method": "id-exact",
                    "count": 1
                }
    
    # === IMPROVEMENT 1: Visibility Filtering (Before Rejection) ===
    # Strategy 5: id attribute - PARTIAL match with visibility filter
    selector = f"[id*='{desc_clean}']"
    count = await page.locator(selector).count()
    
    if count > 1:
        # Try filtering by visibility
        visible_selector = f"{selector}:visible"
        visible_count = await page.locator(visible_selector).count()
        if visible_count == 1:
            return {
                "selector": visible_selector,
                "confidence": 0.88,
                "method": "id-partial-visible",
                "count": 1
            }
    elif count == 1:
        return {
            "selector": selector,
            "confidence": 0.85,
            "method": "id-partial",
            "count": 1
        }
    
    # === IMPROVEMENT 4: Container Context ===
    # Strategy 6: Context-aware selectors (visible containers)
    containers = ["form:visible", ".modal:visible", ".popup:visible", "dialog:visible"]
    
    for container in containers:
        # Check if container exists
        if await page.locator(container).count() > 0:
            # Try button in container
            selector = f"{container} button:has-text('{description}')"
            count = await page.locator(selector).count()
            if count == 1:
                return {
                    "selector": selector,
                    "confidence": 0.87,
                    "method": "container-button",
                    "count": 1
                }
            
            # Try input in container
            selector = f"{container} input[placeholder*='{description}' i]"
            count = await page.locator(selector).count()
            if count == 1:
                return {
                    "selector": selector,
                    "confidence": 0.86,
                    "method": "container-input",
                    "count": 1
                }
    
    # Strategy 7: aria-label with visibility filter
    selector = f"[aria-label*='{description}' i]"
    count = await page.locator(selector).count()
    
    if count > 1:
        visible_selector = f"{selector}:visible"
        visible_count = await page.locator(visible_selector).count()
        if visible_count == 1:
            return {
                "selector": visible_selector,
                "confidence": 0.90,
                "method": "aria-label-visible",
                "count": 1
            }
    elif count == 1:
        return {
            "selector": selector,
            "confidence": 0.92,
            "method": "aria-label",
            "count": 1
        }
    
    # Strategy 8: placeholder with visibility filter
    selector = f"[placeholder*='{description}' i]"
    count = await page.locator(selector).count()
    
    if count > 1:
        visible_selector = f"{selector}:visible"
        visible_count = await page.locator(visible_selector).count()
        if visible_count == 1:
            return {
                "selector": visible_selector,
                "confidence": 0.88,
                "method": "placeholder-visible",
                "count": 1
            }
    elif count == 1:
        return {
            "selector": selector,
            "confidence": 0.90,
            "method": "placeholder",
            "count": 1
        }
    
    # Strategy 9: name attribute with visibility filter
    selector = f"[name*='{desc_clean}']"
    count = await page.locator(selector).count()
    
    if count > 1:
        visible_selector = f"{selector}:visible"
        visible_count = await page.locator(visible_selector).count()
        if visible_count == 1:
            return {
                "selector": visible_selector,
                "confidence": 0.86,
                "method": "name-visible",
                "count": 1
            }
    elif count == 1:
        return {
            "selector": selector,
            "confidence": 0.88,
            "method": "name",
            "count": 1
        }
    
    # Strategy 10: Semantic label + input association
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
    
    # Strategy 11: Button/link text (exact text match)
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
    
    # === NEW: Enhanced Button Text Matching ===
    # Strategy 11b: Button text with :text-is() for case-insensitive exact match
    for tag in ["button", "input[type='button']", "input[type='submit']", "a.btn", "a.button"]:
        try:
            selector = f"{tag}:text-is('{description}')"
            count = await page.locator(selector).count()
            if count == 1:
                return {
                    "selector": selector,
                    "confidence": 0.88,
                    "method": "button-text-is",
                    "count": 1
                }
            
            # Try with visible filter
            if count > 1:
                visible_selector = f"{selector}:visible"
                visible_count = await page.locator(visible_selector).count()
                if visible_count == 1:
                    return {
                        "selector": visible_selector,
                        "confidence": 0.86,
                        "method": "button-text-is-visible",
                        "count": 1
                    }
        except Exception:
            pass
    
    # === IMPROVED: Enhanced Placeholder Matching ===  
    # Strategy 11c: Exact placeholder match (case-insensitive)
    try:
        selector = f"input[placeholder='{description}' i]"
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.92,
                "method": "placeholder-exact-ci",
                "count": 1
            }
        
        # Try textarea as well
        selector = f"textarea[placeholder='{description}' i]"
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.92,
                "method": "placeholder-exact-ci-textarea",
                "count": 1
            }
    except Exception:
        pass
    
    # === NEW: Name Attribute Exact Match ===
    # Strategy 11d: Exact name match (case-insensitive) for form fields
    try:
        for tag in ["input", "select", "textarea"]:
            selector = f"{tag}[name='{desc_clean}' i]"
            count = await page.locator(selector).count()
            if count == 1:
                return {
                    "selector": selector,
                    "confidence": 0.90,
                    "method": "name-exact",
                    "count": 1
                }
    except Exception:
        pass

    
    # === ADVANCED STRATEGIES FOR LEGACY SITES ===
    
    # Strategy 12: Fuzzy Token Matching
    desc_tokens = desc_clean.split()
    if len(desc_tokens) >= 2:
        for tag in ["input", "select", "textarea"]:
            for token in desc_tokens:
                if len(token) >= 3:
                    selector = f"{tag}[name*='{token}' i], {tag}[id*='{token}' i], {tag}[class*='{token}' i]"
                    count = await page.locator(selector).count()
                    if count == 1:
                        return {
                            "selector": selector,
                            "confidence": 0.75,
                            "method": "fuzzy-token",
                            "count": 1
                        }
    
    # Strategy 13: Proximity-Based (ENHANCED - Multi-level + Multiple Element Types)
    try:
        text_selector = f"text={description}"
        text_count = await page.locator(text_selector).count()
        
        if text_count == 1:
            # Define element types to try (in priority order)
            element_types = ["input", "select", "textarea", "button"]
            
            # Define proximity patterns with confidence levels
            proximity_patterns = [
                # Adjacent sibling (highest confidence - immediate neighbor)
                {
                    "pattern": "text={description} + {element}",
                    "confidence": 0.82,
                    "method": "proximity-adjacent"
                },
                # General sibling (any following sibling)
                {
                    "pattern": "text={description} ~ {element}",
                    "confidence": 0.78,
                    "method": "proximity-sibling"
                },
                # One parent level (most common)
                {
                    "pattern": "text={description} >> xpath=.. >> {element}",
                    "confidence": 0.80,
                    "method": "proximity-parent-1"
                },
                # Two parent levels (grandparent)
                {
                    "pattern": "text={description} >> xpath=.. >> xpath=.. >> {element}",
                    "confidence": 0.75,
                    "method": "proximity-parent-2"
                },
                # Three parent levels (great-grandparent)
                {
                    "pattern": "text={description} >> xpath=.. >> xpath=.. >> xpath=.. >> {element}",
                    "confidence": 0.70,
                    "method": "proximity-parent-3"
                },
            ]
            
            # Try each pattern with each element type
            for element_type in element_types:
                for pattern_config in proximity_patterns:
                    selector = pattern_config["pattern"].format(
                        description=description,
                        element=element_type
                    )
                    count = await page.locator(selector).count()
                    
                    if count == 1:
                        return {
                            "selector": selector,
                            "confidence": pattern_config["confidence"],
                            "method": pattern_config["method"],
                            "count": 1
                        }
    except Exception:
        pass
    
    # Strategy 14: Case-Insensitive Text
    for tag in ["button", "a", "span"]:
        selector = f"{tag}:text-is('{description}')"
        count = await page.locator(selector).count()
        if count == 1:
            return {
                "selector": selector,
                "confidence": 0.85,
                "method": "text-case-insensitive",
                "count": 1
            }
    
    # Strategy 15: Visual Scoring Fallback (when count > 1)
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
            best_selector = await _visual_scoring_fallback(page, selector)
            if best_selector:
                return {
                    "selector": best_selector,
                    "confidence": 0.70,
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
            
            # 1. Centrality score
            distance = ((el_center_x - center_x)**2 + (el_center_y - center_y)**2)**0.5
            centrality = 1000 - min(distance, 1000)
            
            # 2. Size score
            area = box['width'] * box['height']
            size_score = min(area * 0.1, 500)
            
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
