"""
Deterministic Code Generator
Inspired by Playwright's codegen - generates test code from traces without LLM
"""
import json
import re
from typing import Dict, List, Any, Optional
from collections import defaultdict


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
        if text:
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
        if tag and text:
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
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Handle Unicode characters that might cause issues
        text = text.encode('ascii', 'replace').decode('ascii')
        # Escape quotes
        text = text.replace('"', '\\"')
        # Truncate if too long
        if len(text) > 100:
            text = text[:97] + '...'
        return text
    
    def _convert_to_css_fallback(self, locator: str, tag: str, text: str) -> str:
        """Convert complex locator to simple CSS"""
        # Extract CSS selector if present
        if 'locator(' in locator:
            match = re.search(r'locator\(["\']([^"\']+)["\']\)', locator)
            if match:
                return f'page.locator("{match.group(1)}")'
        
        # Build simple CSS
        if tag and text:
            return f'page.locator("{tag}").filter(has_text="{self._escape_text(text)}")'
        
        return locator


class ActionMapper:
    """Maps trace actions to Playwright API calls"""
    
    def __init__(self):
        self.action_templates = {
            'click': '{locator}.click()',
            'fill': '{locator}.fill("{value}")',
            'select': '{locator}.select_option("{value}")',
            'check': '{locator}.check()',
            'uncheck': '{locator}.uncheck()',
            'navigate': 'page.goto("{url}")',
            'wait': 'page.wait_for_load_state("networkidle")'
        }
    
    
    def map_action(self, step: Dict[str, Any], locator: str) -> str:
        """
        Map a trace action to Playwright code.
        
        Args:
            step: Trace step with action type and value
            locator: Translated Playwright locator
            
        Returns:
            Playwright action code
        """
        action_type = step.get('action', '')
        value = step.get('value', '')
        url = step.get('url', '')
        element_context = step.get('element_context', {})
        tag = element_context.get('tag', '')
        
        # Special case: navigate action
        if action_type == 'navigate':
            if value:  # value contains target URL
                return f'page.goto("{value}")'
            return f'page.goto("{url}")'
        
        # Check if we should handle new tab (target="_blank" or external link behavior)
        # Note: Trace doesn't always have 'target' attribute, but we can infer from context
        # If it's a link and goal implies checking multiple items, it's safer to handle potential new tabs
        is_link_click = action_type == 'click' and tag == 'a'
        
        # Get template
        template = self.action_templates.get(action_type, '{locator}.click()')
        
        # Fill template
        action_code = template.format(
            locator=locator,
            value=value.replace('"', '\\"') if value else '',
            url=url
        )
        
        # If it's a link click that matches known "new tab" patterns (like 'Try Claude'), handle it
        # Since we can't know for sure from trace, we adding a robust pattern for specific items
        # OR we can wrap all top-level menu clicks in a "try/expect popup" block?
        # A simpler approach: if the next step is on the same URL, we should ensure we are there.
        
        # For this specific task, hitting "Claude" (Index 1) opens new tab.
        # We'll use a heuristic: if we are verifying menu items, assume new tabs should be closed.
        if is_link_click:
             return f'''with page.context.expect_page() as new_page_info:
        {action_code}
    # Handle potential new tab/window
    try:
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass  # If no new page opened, just continue'''
        
        return action_code

class POMBuilder:
    """Builds Page Object Model classes from trace"""
    
    def __init__(self):
        self.locator_translator = LocatorTranslator()
    
    def build_pom_classes(self, trace: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Build POM classes from trace.
        
        Args:
            trace: List of trace steps
            
        Returns:
            Dict of page_name -> {locators, methods}
        """
        pages = defaultdict(lambda: {'locators': {}, 'actions': []})
        
        for step in trace:
            page_name = step.get('page_name', 'UnknownPage')
            action = step.get('action', '')
            
            # Skip navigate actions for POM
            if action == 'navigate':
                continue
            
            # Translate locator
            locator = self.locator_translator.translate(step)
            
            # Create locator name
            locator_name = self._create_locator_name(step)
            
            # Store locator (avoid duplicates)
            if locator_name not in pages[page_name]['locators']:
                pages[page_name]['locators'][locator_name] = {
                    'selector': locator,
                    'description': step.get('thought', ''),
                    'element': step.get('element_context', {})
                }
            
            # Store action
            pages[page_name]['actions'].append({
                'step': step.get('step'),
                'action': action,
                'locator_name': locator_name,
                'value': step.get('value'),
                'thought': step.get('thought', '')
            })
        
        return dict(pages)
    
    def _create_locator_name(self, step: Dict[str, Any]) -> str:
        """Create a semantic locator property name"""
        element_context = step.get('element_context', {})
        text = element_context.get('text', '')
        tag = element_context.get('tag', '')
        action = step.get('action', '')
        
        # Sanitize text for property name
        clean_text = re.sub(r'[^a-zA-Z0-9]+', '_', text.lower())
        clean_text = clean_text.strip('_')[:30]  # Max 30 chars
        
        # Build name based on element type
        if tag == 'input':
            return f'{clean_text}_input' if clean_text else f'{action}_input'
        elif tag == 'button':
            return f'{clean_text}_button' if clean_text else f'{action}_button'
        elif tag == 'a':
            return f'{clean_text}_link' if clean_text else f'{action}_link'
        elif clean_text:
            return f'{clean_text}_{tag}'
        else:
            return f'{action}_{tag or "element"}'
    
    def generate_pom_code(self, page_name: str, page_data: Dict[str, Any]) -> str:
        """Generate POM class code"""
        locators = page_data.get('locators', {})
        
        code = [
            f'class {page_name}:',
            f'    """Auto-generated Page Object for {page_name}"""',
            '    def __init__(self, page: Page):',
            '        self.page = page',
            ''
        ]
        
        # Add locator properties
        for name, data in locators.items():
            selector = data['selector'].replace('page.', 'self.page.')
            description = data.get('description', '')[:100]
            
            code.append('    @property')
            code.append(f'    def {name}(self):')
            if description:
                code.append(f'        """{description}"""')
            code.append(f'        return {selector}')
            code.append('')
        
        return '\n'.join(code)


class TestBuilder:
    """Builds test functions from trace"""
    
    def __init__(self):
        self.action_mapper = ActionMapper()
        self.locator_translator = LocatorTranslator()
    
    def build_test(self, trace_data: Dict[str, Any], pom_classes: Dict[str, Dict]) -> str:
        """
        Build test function code.
        
        Args:
            trace_data: Full trace with workflow, target_url, trace steps
            pom_classes: POM classes built from trace
            
        Returns:
            Test function code
        """
        workflow = trace_data.get('workflow', '')
        target_url = trace_data.get('target_url', '')
        trace = trace_data.get('trace', [])
        
        code = [
            'def test_autonomous_flow(page: Page):',
            f'    """',
            f'    Workflow: {workflow}',
            f'    """',
            f'    # Navigate to target URL',
            f'    page.goto("{target_url}")',
            ''
        ]
        
        # Instantiate page objects
        for page_name in pom_classes.keys():
            var_name = self._to_snake_case(page_name)
            code.append(f'    {var_name} = {page_name}(page)')
        
        code.append('')
        code.append('    # Execute test steps')
        
        # Generate test steps
        for step in trace:
            action_code = self._generate_step_code(step, pom_classes)
            if action_code:
                thought = step.get('thought', '')[:80]
                code.append(f'    # Step {step["step"]}: {thought}')
                # Indent all lines of action code
                for line in action_code.split('\n'):
                    code.append(f'    {line}')
                code.append('')
        
        return '\n'.join(code)
    
    def _generate_step_code(self, step: Dict[str, Any], pom_classes: Dict) -> str:
        """Generate code for a single step"""
        action = step.get('action', '')
        page_name = step.get('page_name', 'UnknownPage')
        
        # Handle navigate action directly
        if action == 'navigate':
            url = step.get('value') or step.get('url')
            return f'page.goto("{url}")'
        
        # For other actions, use POM
        if page_name not in pom_classes:
            # Fallback: direct Playwright call
            locator = self.locator_translator.translate(step)
            return self.action_mapper.map_action(step, locator)
        
        # Use POM
        var_name = self._to_snake_case(page_name)
        locator_name = self._find_matching_locator(step, pom_classes[page_name])
        
        if not locator_name:
            return ''
        
        # Map action
        value = step.get('value', '')
        if action == 'fill':
            return f'{var_name}.{locator_name}.fill("{value}")'
        elif action == 'click':
            click_code = f'{var_name}.{locator_name}.click()'
            # Check for new tab handling (same as ActionMapper)
            tag = step.get('element_context', {}).get('tag', '')
            if tag == 'a':
                 return f'''with page.context.expect_page() as new_page_info:
    {click_code}
    # Handle potential new tab/window
    try:
        new_page = new_page_info.value
        new_page.close()
    except Exception:
        pass'''
            return click_code
        elif action == 'select':
            return f'{var_name}.{locator_name}.select_option("{value}")'
        
        return f'{var_name}.{locator_name}.{action}()'
    
    def _find_matching_locator(self, step: Dict, page_data: Dict) -> Optional[str]:
        """Find matching locator name for step"""
        step_num = step.get('step')
        locators = page_data.get('locators', {})
        actions = page_data.get('actions', [])
        
        # Find action with matching step number
        for action in actions:
            if action.get('step') == step_num:
                return action.get('locator_name')
        
        return None
    
    def _to_snake_case(self, name: str) -> str:
        """Convert PascalCase to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class DeterministicCodeGenerator:
    """
    Main class for deterministic code generation.
    Replaces LLM-based code generation with rule-based approach.
    """
    
    def __init__(self):
        self.pom_builder = POMBuilder()
        self.test_builder = TestBuilder()
    
    def generate_from_trace(self, trace_path: str) -> str:
        """
        Generate test code from trace JSON file.
        
        Args:
            trace_path: Path to trace.json file
            
        Returns:
            Complete test code with POM classes and test function
        """
        # Load trace
        with open(trace_path, 'r', encoding='utf-8') as f:
            trace_data = json.load(f)
        
        # Build POM classes
        pom_classes = self.pom_builder.build_pom_classes(trace_data.get('trace', []))
        
        # Generate code
        code_parts = []
        
        # Imports
        code_parts.append(self._generate_imports())
        code_parts.append('')
        
        # POM classes
        for page_name, page_data in pom_classes.items():
            pom_code = self.pom_builder.generate_pom_code(page_name, page_data)
            code_parts.append(pom_code)
            code_parts.append('')
        
        # Test function
        test_code = self.test_builder.build_test(trace_data, pom_classes)
        code_parts.append(test_code)
        
        return '\n'.join(code_parts)
    
    def _generate_imports(self) -> str:
        """Generate import statements"""
        return '''import sys
import os
sys.path.append(os.getcwd())

from playwright.sync_api import Page, expect
import re

try:
    from helpers import take_screenshot
except ImportError:
    def take_screenshot(page, name, project_name):
        pass  # Fallback if helpers not available'''


if __name__ == '__main__':
    import sys
    
    # Ensure UTF-8 encoding for output
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("Usage: python deterministic_generator.py <trace_path>")
        sys.exit(1)
    
    trace_path = sys.argv[1]
    generator = DeterministicCodeGenerator()
    code = generator.generate_from_trace(trace_path)
    
    print(code)
