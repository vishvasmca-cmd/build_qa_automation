from typing import Optional, Dict

class LocatorInference:
    """
    Infers Playwright locators from semantic field names.
    Used when DSL provides a high-level field name (e.g. 'username')
    instead of a raw locator.
    """
    
    # Common patterns for standard fields
    HEURISTICS = {
        'username': [
            "[name='username']", 
            "[name='email']", 
            "[id='user-name']", 
            "input[placeholder*='user' i]"
        ],
        'password': [
            "[name='password']", 
            "[id='password']", 
            "input[placeholder*='pass' i]"
        ],
        'search': [
            "[name='q']", 
            "[name='search']", 
            "input[placeholder*='search' i]"
        ],
        'submit': [
            "button[type='submit']",
            "input[type='submit']"
        ]
    }
    
    def infer(self, field_name: str, domain: Optional[str] = None) -> str:
        """
        Suggest a locator for a given field name.
        
        Args:
            field_name: Semantic name (e.g., 'username', 'first_name')
            domain: Optional, for future knowledge base lookup
            
        Returns:
            Best guess Playwright locator string
        """
        # 1. Normalize
        key = field_name.lower().strip()
        
        # 2. Check heuristics
        if key in self.HEURISTICS:
            # For now, return the first heuristic. 
            # In future, this could be intelligent based on page source.
            return self.HEURISTICS[key][0]
            
        # 3. Fallback: Generic attribute search
        # Try finding by name attribute first
        return f"[name='{field_name}']"

    def is_semantic_name(self, current_locator: str) -> bool:
        """
        Check if a string looks like a semantic name rather than a locator.
        E.g. "username" vs "[name='username']"
        """
        if any(c in current_locator for c in ['[', '#', '.', '>', ':']):
            return False
        return True
