"""
Helper for logging smart selector attempts

This provides a clean way to log each strategy attempt without cluttering smart_locator.py
"""

def log_attempt(strategy_name: str, selector: str, count: int, debug: bool = True):
    """Log a strategy attempt with result"""
    if not debug:
        return
    
    if count == 1:
        status = "✅"
        result = "MATCH"
    elif count > 1:
        status = "⚠️"
        result = f"{count} matches (need 1)"
    else:
        status = "❌"
        result = "0 matches"
    
    print(f"      {status} [{strategy_name:20s}] {selector:50s} → {result}")
    
    return count == 1  # Return True if successful


def log_final(strategies_tried: int, debug: bool = True):
    """Log final result after all strategies failed"""
    if not debug:
        return
        
    print(f"    ❌ [SMART] All {strategies_tried} strategies failed → AI Vision fallback")
