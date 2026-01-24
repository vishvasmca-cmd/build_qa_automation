"""
Smart Locator Module - Enhanced with AI Gap Improvements

This module provides intelligent element location strategies that try
deterministic methods before falling back to expensive AI vision calls.

IMPROVEMENTS (v2.0):
- Visibility filtering (count > 1 -> check :visible)
- Exact ID matching before partial  
- Role locators as high priority
- Container context awareness
- First-item e-commerce patterns

Target: 93% success rate on modern sites (up from 85%)
"""

from typing import Optional, Dict, List, Any
from playwright.async_api import Page
import re
import json
import os

# Debug mode - set to True to see detailed strategy attempts
DEBUG_SMART_SELECTORS = True

# Early exit optimization: Stop trying strategies after finding high-confidence match
# This can save 60-80% of execution time in common cases
CONFIDENCE_THRESHOLD_EARLY_EXIT = 0.92  # Return immediately if confidence >= this

# Helper function for CSS escaping
def _css_escape(identifier: str) -> str:
    """
    Escape special characters in CSS identifiers.
    Handles: spaces, /, (, ), [, ], etc.
    """
    # Characters that need escaping in CSS selectors
    special_chars = r'[ !/"#$%&\'()*+,./:;<=>?@[\\\]^`{|}~]'
    
    def escape_char(match):
        char = match.group(0)
        # Escape with backslash and space
        return f'\\{ord(char):x} '
    
    return re.sub(special_chars, escape_char, identifier).rstrip()


def sanitize_ai_selector(selector: str) -> str:
    """
    Sanitize AI-suggested selectors to prevent Playwright SyntaxErrors.
    Fixes common LLM hallucinations like :contains(), raw text, or unescaped characters.
    """
    if not selector:
        return selector
    
    # 1. Remove unsupported :contains() - usually meant to be :has-text() or text=
    if ":contains(" in selector:
        # Extract the text from :contains('text')
        match = re.search(r":contains\(['\"]?(.*?)['\"]?\)", selector)
        if match:
            text_val = match.group(1)
            # Replace with Playwright's preferred text= or :has-text()
            # If it's a simple tag like 'a:contains', we can change it to 'text=text'
            base_tag = selector.split(":contains")[0]
            if base_tag and base_tag != "*":
                selector = f"{base_tag}:has-text('{text_val}')"
            else:
                selector = f"text='{text_val}'"
    
    # 2. Fix unescaped hashes/dots in descriptions that aren't real selectors
    # e.g. "Click #1 button" -> text="Click #1 button"
    if selector.startswith('#') and ' ' in selector:
        selector = f"text='{selector}'"
        
    return selector


async def find_element_smart(page: Page, description: str, debug: bool = None) -> Optional[Dict]:
    """
    Try deterministic element finding strategies before AI fallback.
    
    Enhanced with 5 AI gap improvements for 85% -> 93% success rate.
    
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
    
    candidates = []
    strategies_tried = 0
    
    if debug:
        print(f"    [SEARCH] Searching for: '{description}' (optimized order: ID -> Role -> Name -> Text)")
    
    # === SANITIZATION FIX: Strip newlines/tabs to prevent "BADSTRING" errors ===
    if not description:
        return None
    
    # 1. Strip whitespace/newlines
    description = description.strip().replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    
    # 2. Escape quotes for attribute/text selectors (prevent syntax errors)
    # e.g., "Men's" -> "Men\'s"
    safe_desc = description.replace("'", "\\'")
    
    # Normalize for matching
    desc_lower = description.lower()
    desc_clean = re.sub(r'[^a-z0-9\s]', '', desc_lower)  # Remove special chars
    desc_with_separators = description.lower()  # Keep underscores/dashes for technical IDs
    
    # === CRITICAL FIX: Detect CSS selectors to avoid parsing errors ===
    is_css_selector = (
        description.startswith(('div[', 'span[', 'button[', 'a[', 'input[', '#', '.')) or
        re.search(r'\[class\s*[=*^$~|]', description) or  # Matches [class=...] patterns
        re.search(r'\[id\s*[=*^$~|]', description) or     # Matches [id=...] patterns
        re.search(r'\[.*\s*=\s*["\']', description)       # Matches any [attr="..."] patterns
    )
    
    if debug and is_css_selector:
        print(f"    [WARN] [SMART] Detected CSS selector syntax in '{description}' - skipping role/link strategies")
    
    # === STRATEGIES (OPTIMIZED ORDER BY SUCCESS RATE) ===
    # Performance ranking from CI analysis:
    # 1. id-exact: 35.3%
    # 2. as-is-#: 9.8%  
    # 3. role-*: 9.8%
    # 4. name: 7.8%
    # 5. text-is: 7.8%
    
    # Strategy 1: ID-exact (35% success rate - HIGHEST PERFORMER)
    id_variations = [
        desc_with_separators,  # Try original with underscores/dashes first
        desc_clean.replace(' ', '_'),
        desc_clean.replace(' ', '-'),
        desc_clean.replace(' ', ''),
        ''.join(word.capitalize() for word in desc_clean.split()) if ' ' in desc_clean else desc_clean
    ]
    for id_var in id_variations:
        if id_var:
            try:
                escaped_id = _css_escape(id_var)
                sel = f"#{escaped_id}"
                count = await page.locator(sel).count()
                if debug:
                    print(f"      [1] id-exact: '{sel}' -> {count} matches")
                if count == 1:
                    # HIGH CONFIDENCE - Return immediately (no need to try other strategies)
                    if debug:
                        print(f"      [OK] EARLY EXIT: High confidence match found!")
                    return {"selector": sel, "confidence": 0.92, "method": "id-exact", "count": 1}
            except Exception as e:
                if debug:
                    print(f"      [1] id-exact: ERROR - {str(e)[:80]}")
    
    # Strategy 1.5: Data-test/testid Attributes (SauceDemo, Modern Web)
    data_attrs = ["data-test", "data-testid", "data-qa", "qa-id", "test-id"]
    if not is_css_selector:
        for attr in data_attrs:
            # Try variations matching description
            attr_variations = [
                desc_with_separators,
                desc_clean.replace(' ', '_'),
                desc_clean.replace(' ', '-'),
                desc_clean.replace(' ', '')
            ]
            for val in attr_variations:
                if not val: continue
                try:
                    # Case insensitive partial match for robustness
                    sel = f"[{attr}*='{val}' i]"
                    count = await page.locator(sel).count()
                    if debug: print(f"      [1.5] {attr}: '{sel}' -> {count} matches")
                    if count == 1:
                        # HIGH CONFIDENCE - Return immediately
                        if debug: print(f"      [OK] EARLY EXIT: Data attribute match!")
                        return {"selector": sel, "confidence": 0.95, "method": f"{attr}-match", "count": 1}
                    elif count > 1:
                        # Collection support - pick best via visual scoring
                        best_sel = await _visual_scoring_fallback(page, sel)
                        if best_sel:
                            candidates.append({"selector": best_sel, "confidence": 0.88, "method": f"{attr}-disambiguated", "count": 1})
                        else:
                            candidates.append({"selector": sel, "confidence": 0.82, "method": f"{attr}-multi", "count": count})
                except: pass

    # Strategy 2: Role Locators (10% success, 0.96 confidence - PROMOTED)
    # Moved earlier due to high confidence and modern web standards
    if not is_css_selector:
        # Ordinal generic
        ordinal_selector = _handle_ordinals(description)
        if ordinal_selector:
            try:
                base_part = ordinal_selector.split(" >> ")[0]
                count = await page.locator(base_part).count()
                if debug:
                    print(f"      [1] ordinal-generic: '{ordinal_selector}' -> {count} matches")
                if count >= 1:
                    candidates.append({
                        "selector": ordinal_selector,
                        "confidence": 0.88,
                        "method": "ordinal-generic",
                        "count": 1
                    })
            except Exception as e:
                if debug:
                    print(f"      [1] ordinal-generic: ERROR - {str(e)[:50]}")
            
        role_mappings = {
            "button": ["button", "submit", "login", "register", "search", "add", "continue", "checkout", "proceed", "purchase", "buy"],
            "link": ["link", "navigate", "view", "details", "cart", "product"],
            "textbox": ["email", "password", "username", "search", "name", "address", "city", "zip", "phone", "first", "last"],
        }
        for role, keywords in role_mappings.items():
            if any(kw in desc_lower for kw in keywords):
                # Exact match
                # FIX: Use safe_desc to handle quotes
                sel = f"role={role}[name='{safe_desc}' i]"
                try:
                    count = await page.locator(sel).count()
                    if debug:
                        print(f"      [2] role-{role}-exact: '{sel}' -> {count} matches")
                    if count == 1:
                        # HIGHEST CONFIDENCE - Return immediately
                        if debug:
                            print(f"      [OK] EARLY EXIT: Role match (0.96 confidence)!")
                        return {"selector": sel, "confidence": 0.96, "method": f"role-{role}-exact", "count": 1}
                except Exception as e:
                    if debug:
                        print(f"      [2] role-{role}-exact: ERROR - {str(e)[:50]}")
                
                # Partial match
                # FIX: Use safe_desc
                sel = f"role={role}[name*='{safe_desc}' i]"
                try:
                    count = await page.locator(sel).count()
                    if count > 50:  # Increased limit for collection items
                        if debug: print(f"      [WARN] [2] Too ambiguous ({count} matches). Skipping.")
                        continue
                        
                    if debug:
                        print(f"      [2] role-{role}-partial: '{sel}' -> {count} matches")
                    if count == 1:
                        candidates.append({"selector": sel, "confidence": 0.93, "method": f"role-{role}-partial", "count": 1})
                    elif count > 1:
                        # Collection support - pick best via visual scoring
                        best_sel = await _visual_scoring_fallback(page, sel)
                        if best_sel:
                            candidates.append({"selector": best_sel, "confidence": 0.85, "method": f"role-{role}-disambiguated", "count": 1})
                except Exception as e:
                    if debug:
                        print(f"      [2] role-{role}-partial: ERROR - {str(e)[:50]}")
    
    # Strategy 3: as-is technical IDs (10% success rate)
    if not is_css_selector and ('_' in description or '-' in description):
        for prefix in ['#', '.', '']:
            sel = f"{prefix}{desc_with_separators}"
            try:
                count = await page.locator(sel).count()
                if debug:
                    prefix_label = prefix if prefix else 'tag'
                    print(f"      [3] as-is-{prefix_label}: '{sel}' -> {count} matches")
                if count == 1:
                    # HIGH CONFIDENCE - Return immediately
                    if debug:
                        print(f"      [OK] EARLY EXIT: as-is match (0.95 confidence)!")
                    return {"selector": sel, "confidence": 0.95, "method": f"as-is-{prefix or 'tag'}", "count": 1}
            except Exception as e:
                if debug:
                    print(f"      [3] as-is: ERROR - {str(e)[:50]}")
    
    # Strategy 4: Ordinal selectors (6% success rate)
    if not is_css_selector:
        ordinal_selector = _handle_ordinals(description)
        if ordinal_selector:
            try:
                base_part = ordinal_selector.split(" >> ")[0]
                count = await page.locator(base_part).count()
                if debug:
                    print(f"      [4] ordinal-generic: '{ordinal_selector}' -> {count} matches")
                if count >= 1:
                    candidates.append({
                        "selector": ordinal_selector,
                        "confidence": 0.88,
                        "method": "ordinal-generic",
                        "count": 1
                    })
            except Exception as e:
                if debug:
                    print(f"      [4] ordinal-generic: ERROR - {str(e)[:50]}")
                
    try:
        sel = f"[id*='{desc_clean}']"
        count = await page.locator(sel).count()
        if debug:
            print(f"      [8] id-partial: '{sel}' -> {count} matches")
        if count == 1:
            candidates.append({"selector": sel, "confidence": 0.85, "method": "id-partial", "count": 1})
        elif count > 1:
            # FIX 2: Add visibility check for strict mode prevention
            sel_vis = f"{sel}:visible"
            count_vis = await page.locator(sel_vis).count()
            if debug:
                print(f"      [9] id-partial-visible: '{sel_vis}' -> {count_vis} matches")
            if count_vis == 1:
                candidates.append({"selector": sel_vis, "confidence": 0.88, "method": "id-partial-visible", "count": 1})
    except Exception as e:
        if debug:
            print(f"      [8] id-partial: ERROR - {str(e)[:80]}")
             
    # Strategy 6: Context Containers
    containers = ["form:visible", ".modal:visible", "dialog:visible"]
    for container in containers:
        if await page.locator(container).count() > 0:
            sel = f"{container} button:has-text('{safe_desc}')"
            if await page.locator(sel).count() == 1:
                candidates.append({"selector": sel, "confidence": 0.87, "method": "container-button", "count": 1})
            sel = f"{container} input[placeholder*='{safe_desc}' i]"
            if await page.locator(sel).count() == 1:
                candidates.append({"selector": sel, "confidence": 0.86, "method": "container-input", "count": 1})

    # Strategy 5: Name attributes (8% success rate - GOOD for forms)
    for name_type in ["exact", "partial"]:
        if name_type == "exact":
            sel = f"input[name='{desc_clean}' i]"
            conf, method = 0.90, "name-exact"
        else:
            sel = f"[name*='{desc_clean}' i]"
            conf, method = 0.88, "name"
        
        try:
            count = await page.locator(sel).count()
            if debug:
                print(f"      [5] {method}: '{sel}' -> {count} matches")
            if count == 1:
                candidates.append({"selector": sel, "confidence": conf, "method": method, "count": 1})
        except Exception as e:
            if debug:
                print(f"      [5] {method}: ERROR - {str(e)[:50]}")
    
    # Strategy 6: Placeholder (4% success rate - forms)
    try:
        sel = f"input[placeholder='{safe_desc}' i]"
        count = await page.locator(sel).count()
        if debug:
            print(f"      [6] placeholder-exact-ci: '{sel}' -> {count} matches")
        if count == 1:
            candidates.append({"selector": sel, "confidence": 0.92, "method": "placeholder-exact-ci", "count": 1})
    except:
        pass

    # Strategy 10: Label association
    try:
        sel = f"label:has-text('{safe_desc}') input"
        if await page.locator(sel).count() == 1:
            candidates.append({"selector": sel, "confidence": 0.87, "method": "label-wrapped", "count": 1})
            
        labels = page.locator(f"label:has-text('{safe_desc}')")
        if await labels.count() == 1:
            for_attr = await labels.get_attribute("for")
            if for_attr:
                sel = f"#{for_attr}"
                if await page.locator(sel).count() == 1:
                    candidates.append({"selector": sel, "confidence": 0.87, "method": "label-for", "count": 1})
    except: pass
    
    # Strategy 7: Text-based (8% total, but only button/span work well)
    # REFINED: Tag-specific matching to reduce strict mode violations
    text_strategies = [
        ("button", 0.88),  # Buttons rarely have ambiguous text
        ("span", 0.88),    # Span text worked in CI
        ("a", 0.85),       # Links are okay but less reliable
        # REMOVED: "div" (0% success rate - too generic)
    ]
    
    for tag, base_conf in text_strategies:
        try:
            sel = f"{tag}:text-is('{safe_desc}')"
            count = await page.locator(sel).count()
            if debug:
                print(f"      [7] {tag}-text-is: '{sel}' -> {count} matches")
            
            # === STRICT ORDINAL LIMIT ===
            if count > 20:
                if debug:
                    print(f"      [WARN] [7] Too ambiguous ({count} matches). Skipping to force more specific strategy.")
                continue

            if count == 1:
                candidates.append({"selector": sel, "confidence": base_conf, "method": f"{tag}-text-is", "count": 1})
            elif count > 1:
                # Strict mode prevention: add :visible filter
                sel_vis = f"{sel}:visible"
                try:
                    count_vis = await page.locator(sel_vis).count()
                    if debug:
                        print(f"      [7] {tag}-text-is-visible: '{sel_vis}' -> {count_vis} matches")
                    
                    if count_vis == 1:
                        candidates.append({"selector": sel_vis, "confidence": base_conf - 0.02, "method": f"{tag}-text-is-visible", "count": 1})
                    elif count_vis > 1 and tag == "button":  # Only for buttons
                        # Fallback to first visible button
                        sel_first = f"{sel_vis} >> nth=0"
                        if debug:
                            print(f"      [7] {tag}-first-visible: '{sel_first}' -> fallback")
                        candidates.append({"selector": sel_first, "confidence": 0.75, "method": f"{tag}-text-is-first-visible", "count": 1})
                except Exception as e_vis:
                    if debug:
                        print(f"      [7] {tag}-visible: ERROR - {str(e_vis)[:50]}")
        except Exception as e:
            if debug:
                print(f"      [7] {tag}-text-is: ERROR - {str(e)[:50]}")
        
            # Try Uppercase variation (Common for buttons like ADD TO CART)
            if description.upper() != description:
                try:
                    sel_upper = f"{tag}:text-is('{description.upper()}')"
                    count_upper = await page.locator(sel_upper).count()
                    if debug: print(f"      [7b] {tag}-text-upper: '{sel_upper}' -> {count_upper} matches")
                    if count_upper == 1:
                        candidates.append({"selector": sel_upper, "confidence": base_conf - 0.05, "method": f"{tag}-text-upper", "count": 1})
                except: pass
        
    # Strategy 11c: Exact placeholder/name
    try:
        sel = f"input[placeholder='{safe_desc}' i]"
        if await page.locator(sel).count() == 1:
            candidates.append({"selector": sel, "confidence": 0.92, "method": "placeholder-exact-ci", "count": 1})
            
        sel = f"input[name='{desc_clean}' i]"
        if await page.locator(sel).count() == 1:
             candidates.append({"selector": sel, "confidence": 0.90, "method": "name-exact", "count": 1})
    except: pass
    
    # Strategy 14: Case-insensitive text
    for tag in ["button", "a", "span"]:
        try:
            sel = f"{tag}:text-is('{safe_desc}')"
            if await page.locator(sel).count() == 1:
                candidates.append({"selector": sel, "confidence": 0.85, "method": "text-case-insensitive", "count": 1})
        except: pass
    
    # Strategy 15: Visual Scoring Fallback (when count > 1)
    # Strategy 15: Visual Scoring Fallback (when count > 1)
    fallback_selectors = [
        f"[placeholder*='{safe_desc}' i]",
        f"[aria-label*='{safe_desc}' i]",
        f"button:has-text('{safe_desc}')",
        f"input[name*='{desc_clean}']",
        f"[id*='{desc_clean}']",
    ]
    
    for selector in fallback_selectors:
        count = await page.locator(selector).count()
        if count > 1:
            best_selector = await _visual_scoring_fallback(page, selector)
            if best_selector:
                candidates.append({
                    "selector": best_selector,
                    "confidence": 0.70,
                    "method": "visual-scoring",
                    "count": 1
                })

    # === PHASE 4.5: Goal Context Refinement ===
    # If a goal is provided and we have MULTIPLE candidates, prioritize those that match goal keywords
    # This helps pick "Backpack" add-to-cart among multiple add-to-cart buttons
    try:
        current_goal = os.environ.get("CURRENT_GOAL", "").lower()
        if current_goal and candidates:
            # Extract keywords from goal (simple split)
            goal_keywords = [w for w in re.split(r'[^a-zA-Z0-9]', current_goal) if len(w) > 3]
            for cand in candidates:
                selector = cand["selector"].lower()
                # Boost if selector contains goal keywords
                for kw in goal_keywords:
                    if kw in selector:
                        cand["confidence"] += 0.05
                        if debug: print(f"      [BOOST] [PRIMING] Goal keyword '{kw}' found in selector. Boosting confidence.")
    except Exception as e:
        if debug: print(f"      [WARN] Goal priming error: {e}")

    # === SELECT BEST CANDIDATE ===
    if not candidates:
        return None
        
    # Calculate stability scores for all candidates
    for cand in candidates:
        cand["stability_score"] = _calculate_stability_score(cand["selector"], cand)
        
    # === PHASE 5: History-Based Prioritization ===
    try:
        from urllib.parse import urlparse
        domain = urlparse(page.url).netloc
        candidates = prioritize_by_history(candidates, domain)
    except:
        pass
        
    # Sort by stability score (descending)
    candidates.sort(key=lambda x: x["stability_score"], reverse=True)
    
    # Log TOP 3 (as requested)
    if debug:
        print(f"    [TOP 3] Smart Locators found:")
        for i, cand in enumerate(candidates[:3]):
            score = cand['stability_score']
            bonus = " (+History)" if cand.get("history_bonus") else ""
            print(f"       {i+1}. {cand['selector']} (Score: {score:.2f}{bonus}, Method: {cand['method']})")
            
    # Return best
    best = candidates[0]
    return best


def _calculate_stability_score(locator: str, context: Dict) -> float:
    """Multi-factor stability scoring as requested."""
    score = context.get("confidence", 0.5)  # Start with base confidence
    
    # Factor 1: Selector type
    if 'id=' in locator or locator.startswith('#'):
        score += 0.15  # IDs are stable
    elif 'data-testid=' in locator or 'data-test=' in locator:
        score += 0.20  # Test attributes are stable
    elif 'role=' in locator:
        score += 0.10  # ARIA roles are fairly stable
    
    # Factor 2: Brittle inclusions
    if ':nth-child(' in locator or ':nth-of-type(' in locator:
        # Check if scoped
        if not ("#" in locator or "data-" in locator or len(locator.split(">>")) < 3):
             score -= 0.20  # Unscoped positional is brittle
        else:
             score -= 0.05  # Scoped positional is okayish
             
    if re.search(r'\.css-[a-z0-9]+', locator):  # CSS-in-JS classes
        score -= 0.15
        
    if len(locator.split()) > 6:  # Very complex selectors
        score -= 0.10
        
    return min(max(score, 0.0), 1.0)  # Clamp to [0, 1]


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


def is_diverse_from_existing(new_locator: str, existing_locators: List[str], threshold: float = 0.85) -> bool:
    """
    Checks if a new locator is sufficiently different from existing ones using Jaccard similarity.
    Returns True if diverse (keep it), False if too similar (discard).
    """
    if not existing_locators:
        return True
        
    def _tokenize(s):
        # Split by common CSS delimiters
        return set(re.split(r'[\s>\+\~\.\[\]"#=]+', s))

    new_tokens = _tokenize(new_locator)
    
    for existing in existing_locators:
        # Exact match check
        if new_locator == existing:
            return False
            
        existing_tokens = _tokenize(existing)
        
        # Jaccard Similarity
        intersection = len(new_tokens.intersection(existing_tokens))
        union = len(new_tokens.union(existing_tokens))
        
        if union == 0:
            continue
            
        similarity = intersection / union
        
        if similarity > threshold:
            # Too similar!
            return False
            
    return True


def prioritize_by_history(candidates: List[Dict], domain: str) -> List[Dict]:
    """
    Reorders candidates based on historical success rates from knowledge/locator_patterns.json.
    """
    try:
        # Locate knowledge file relative to this file
        # core/lib/smart_locator.py -> ../../knowledge/locator_patterns.json
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        kb_path = os.path.join(base_dir, "knowledge", "locator_patterns.json")
        
        if not os.path.exists(kb_path):
            return candidates
            
        with open(kb_path, "r", encoding="utf-8") as f:
            patterns = json.load(f)
            
        domain_patterns = patterns.get(domain, {}).get("successful_patterns", [])
        if not domain_patterns:
            return candidates
            
        # Apply bonuses
        for cand in candidates:
            selector = cand["selector"]
            # Check for exact or pattern match
            for pattern in domain_patterns:
                if pattern in selector:
                     cand["stability_score"] += 0.15 # Success bonus
                     cand["history_bonus"] = True
                     break
                     
        # Re-sort
        candidates.sort(key=lambda x: x["stability_score"], reverse=True)
        return candidates
        
    except Exception:
        return candidates

def _handle_ordinals(description: str) -> Optional[str]:
    """
    Convert ordinal descriptions like 'first product', '2nd item' into :nth-child selectors.
    
    Returns:
        Selector string (e.g., '.product >> nth=0') or None if no ordinal found.
    """
    desc_lower = description.lower().strip()
    
    # Map ordinal words to indices
    ordinal_map = {
        "first": 0, "1st": 0,
        "second": 1, "2nd": 1,
        "third": 2, "3rd": 2,
        "fourth": 3, "4th": 3,
        "fifth": 4, "5th": 4,
        "last": -1
    }
    
    # Find ordinal keyword
    found_index = None
    cleaned_desc = desc_lower
    
    for word, index in ordinal_map.items():
        if word in desc_lower:
            found_index = index
            # Remove the ordinal word to get the "base" description
            # e.g., "first product" -> "product"
            cleaned_desc = desc_lower.replace(word, "").strip()
            break
            
    if found_index is None:
        return None
        
    # Heuristic: Map common item names to selectors
    base_selector = None
    
    # 1. Product/Item heuristics
    if any(x in cleaned_desc for x in ["product", "item", "result", "card"]):
        # Try generic list items
        base_selector = ".product, .item, .card, li, div[role='article']"
        
    # 2. Table row heuristics
    elif "row" in cleaned_desc:
        base_selector = "tr"
        
    # 3. List item heuristics
    elif any(x in cleaned_desc for x in ["element", "entry", "option"]):
        base_selector = "li, option, div[role='option']"
        
    # 4. Button/Link heuristics
    elif "button" in cleaned_desc:
        base_selector = "button, input[type='button'], a.btn"
    elif "link" in cleaned_desc:
        base_selector = "a"
        
    # 5. Fallback: Try to use the cleaned description as a class or ID
    if not base_selector:
        # e.g., "first todo-item" -> ".todo-item"
        clean_token = re.sub(r'[^a-z0-9-]', '', cleaned_desc.replace(" ", "-"))
        if clean_token:
            base_selector = f".{clean_token}, [data-test*='{clean_token}'], [id*='{clean_token}']"
            
    if base_selector:
        return f"{base_selector} >> nth={found_index}"
        
    return None
