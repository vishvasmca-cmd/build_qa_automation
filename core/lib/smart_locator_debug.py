"""
Debug wrapper for smart_locator.py to track strategy execution

This wraps the original get_smart_selector to add comprehensive logging
of which strategies are tried and why they succeed/fail.
"""

from typing import Optional, Dict
from playwright.async_api import Page

# Track strategy attempts globally for analysis
strategy_attempts = []


async def get_smart_selector_with_debug(page: Page, description: str, log_func=None):
    """
    Wrapper around get_smart_selector that adds debug logging.
    
    Shows:
    - Which strategies are attempted
    - Why each strategy failed (count == 0, count > 1, etc.)
    - Which strategy succeeded
    - Final outcome (success or fallback to AI)
    """
    debug_log = log_func if log_func else print
    
    debug_log(f"    🔍 [DEBUG] Starting smart selector search for: '{description}'")
    
    # Import the original function
    from core.lib.smart_locator import find_element_smart
    
    # Try to execute with detailed logging
    try:
        result = await find_element_smart(page, description)
        
        if result:
            debug_log(f"    ✅ [DEBUG] SUCCESS via strategy: {result.get('method')} (confidence: {result.get('confidence')})")
            debug_log(f"    📍 [DEBUG] Selector: {result.get('selector')}")
        else:
            debug_log(f"    ❌ [DEBUG] All strategies FAILED - falling back to AI")
       
        return result
        
    except Exception as e:
        debug_log(f"    ⚠️ [DEBUG] Smart selector error: {e}")
        return None


# Simpler approach: Add logging at key checkpoints
def log_strategy_attempt(strategy_name, selector, count, description=""):
    """Log each strategy attempt for debugging"""
    global strategy_attempts
    
    attempt = {
        "strategy": strategy_name,
        "selector": selector,
        "count": count,
        "description": description,
        "result": "MATCH" if count == 1 else ("MULTIPLE" if count > 1 else "NONE")
    }
    
    strategy_attempts.append(attempt)
    
    # Print for real-time debugging
    status = "✅" if count == 1 else ("⚠️" if count > 1 else "❌")
    print(f"      {status} [{strategy_name}] {selector} → {count} elements")
    
    return count == 1  # Return True if unique match
