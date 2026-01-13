import re
from typing import Dict, Any, Optional

class LocatorTranslator:
    """
    Translates trace locators to Playwright best practices following priority hierarchy:
    1. getByRole() - ARIA roles
    2. getByLabel() - Form labels
    3. getByPlaceholder() - Input placeholders  
    4. getByText() - Visible text
    5. getByTestId() - data-testid attributes
    6. locator() - CSS fallback
    """
    
    def __init__(self):
        self.priority_order = [
            'role_based',
            'label_based',
            'placeholder',
            'text_based',
            'test_id',
            'css_fallback'
        ]
    
    def translate(self, step: Dict[str, Any]) -> str:
        """
        Translate a trace step to the best Playwright locator.
        
        Args:
            step: Trace step with action, element_context, locator_used
            
        Returns:
            Playwright locator string
        """
        # If trace already has a good locator, use it (with disambiguation)
        locator_used = step.get('locator_used', '')
        # Try to build from element_context first (Deterministic)
        element_context = step.get('element_context', {})
        if element_context and (element_context.get('text') or element_context.get('role') or element_context.get('fragment')):
             pass # Fall through to context-based generation
        elif locator_used and self._is_good_locator(locator_used):
             # Fallback to trace locator if context is missing
             return self._add_disambiguation(self._clean_locator(locator_used), step)
        
        # Otherwise, build best locator from element_context
        element_context = step.get('element_context', {})
        tag = element_context.get('tag', '')
        text = element_context.get('text', '')
        role = element_context.get('role', '')
        href = element_context.get('href', '')
        data_attrs = {k: v for k, v in element_context.items() if k.startswith('data-')}
        
        # Priority 0: Unique data attributes (best for disambiguation)
        if data_attrs:
            for attr, value in data_attrs.items():
                if attr in ['data-testid', 'data-test', 'data-test-id']:
                    return f'page.get_by_test_id("{value}")'
                # Use other data attributes via CSS selector
                if value and len(value) < 50:
                    return f'page.locator("[{attr}=\\"{value}\\"]")'
        
        # Priority 1: Role-based with exact match for disambiguation
        if role and text:
            base_locator = f'page.get_by_role("{role}", name="{self._escape_text(text)}", exact=True)'
            # For links, add href filter for disambiguation
            if role == 'link' and href:
                return f'{base_locator}.filter(has=page.locator(\'[href="{href}"]\'))'
            return self._add_disambiguation(base_locator, step)
        
        # Infer role from tag if not provided
        inferred_role = self._infer_role(tag, text)
        if inferred_role and text:
            base_locator = f'page.get_by_role("{inferred_role}", name="{self._escape_text(text)}", exact=True)'
            # Add href filter for links
            if inferred_role == 'link' and href:
                return f'{base_locator}.filter(has=page.locator(\'[href="{href}"]\'))'
            return self._add_disambiguation(base_locator, step)
        
        # Priority 2: Label (for inputs)
        if tag == 'input' and 'label' in element_context:
            return f'page.get_by_label("{self._escape_text(element_context["label"])}")'
        
        # Priority 3: Placeholder
        if 'placeholder' in element_context:
            return f'page.get_by_placeholder("{self._escape_text(element_context["placeholder"])}")'
        
        # Check if trace locator has placeholder
        if locator_used and 'get_by_placeholder' in locator_used:
            return self._add_disambiguation(self._clean_locator(locator_used), step)
        
        # Priority 4: Text content with exact match
        if text and tag not in ['input', 'select', 'textarea']:
            # For buttons and links, use exact text
            if tag in ['button', 'a', 'span'] and len(text) < 50:
                base_locator = f'page.get_by_text("{self._escape_text(text)}", exact=True)'
                # For links, add href filter
                if tag == 'a' and href:
                    return f'{base_locator}.filter(has=page.locator(\'[href="{href}"]\'))'
                return self._add_disambiguation(base_locator, step)
        
        # Priority 5: Test ID
        if 'data-testid' in element_context:
            return f'page.get_by_test_id("{element_context["data-testid"]}")'
        
        # Priority 6: CSS fallback with attributes
        if locator_used:
            return self._add_disambiguation(self._convert_to_css_fallback(locator_used, tag, text), step)
        
        # Last resort: generic locator by tag and text with .first
        if tag and text and tag not in ['input', 'select', 'textarea']:
            return f'page.locator("{tag}").filter(has_text="{self._escape_text(text)}").first'
        
        return 'page.locator("body")'  # Fallback
    
    def _add_disambiguation(self, locator: str, step: Dict[str, Any]) -> str:
        """
        Add disambiguation to locator to handle multiple matches.
        Adds .first for ambiguous selectors to prevent strict mode violations.
        
        Args:
            locator: Base Playwright locator
            step: Trace step with context
            
        Returns:
            Locator with disambiguation
        """
        # Don't add .first if locator is already specific
        specific_patterns = [
            'get_by_test_id',
            'get_by_placeholder',
            'get_by_label',
            '.filter(has=',  # Already filtered
            '.first',        # Already has .first
            '.nth(',          # Already has .nth()
        ]
        
        if any(pattern in locator for pattern in specific_patterns):
            return locator
        
        # For role/text-based locators that might match multiple elements
        ambiguous_patterns = [
            'get_by_role',
            'get_by_text'
        ]
        
        if any(pattern in locator for pattern in ambiguous_patterns):
            # Add .first to prevent strict mode violations
            return f'{locator}.first'
        
        return locator
    
    def _is_good_locator(self, locator: str) -> bool:
        """Check if locator already follows best practices"""
        good_patterns = [
            'get_by_role',
            'get_by_label',
            'get_by_placeholder',
            'get_by_text',
            'get_by_test_id'
        ]
        return any(pattern in locator for pattern in good_patterns)
    
    def _clean_locator(self, locator: str) -> str:
        """Clean and normalize locator string"""
        # Remove 'page.' prefix if present
        locator = locator.replace('page.', '')
        
        # Ensure it starts with 'page.'
        if not locator.startswith('page.'):
            locator = 'page.' + locator
        
        return locator
    
    def _infer_role(self, tag: str, text: str) -> Optional[str]:
        """Infer ARIA role from HTML tag"""
        role_map = {
            'button': 'button',
            'a': 'link',
            'input[type="checkbox"]': 'checkbox',
            'input[type="radio"]': 'radio',
            'select': 'combobox',
            'textarea': 'textbox',
            'img': 'img',
            'h1': 'heading',
            'h2': 'heading',
            'h3': 'heading'
        }
        return role_map.get(tag)
    
    def _escape_text(self, text: str) -> str:
        """Escape special characters in text"""
        # Escape backslashes first, then quotes
        text = text.replace('\\', '\\\\').replace('"', '\\"')
        # Normalize whitespace
        text = ' '.join(text.split())
        # Truncate if too long (optional, but keep it for stability)
        if len(text) > 100:
            text = text[:97] + '...'
        return text
    
    def _convert_to_css_fallback(self, locator: str, tag: str, text: str) -> str:
        """Convert complex locator to simple CSS"""
        # Extract CSS selector if present
        if 'locator(' in locator or 'get_by_' in locator:
            return locator
        
        # Build simple CSS
        if tag and text:
            return f'page.locator("{tag}").filter(has_text="{self._escape_text(text)}")'
        
        return locator
