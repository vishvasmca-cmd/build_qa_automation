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
        # If trace already has a good locator, use it
        locator_used = step.get('locator_used', '')
        if locator_used and self._is_good_locator(locator_used):
            return self._clean_locator(locator_used)
        
        # Otherwise, build best locator from element_context
        element_context = step.get('element_context', {})
        tag = element_context.get('tag', '')
        text = element_context.get('text', '')
        role = element_context.get('role', '')
        
        # Priority 1: Role-based (best)
        if role and text:
            return f'page.get_by_role("{role}", name="{self._escape_text(text)}")'
        
        # Infer role from tag if not provided
        inferred_role = self._infer_role(tag, text)
        if inferred_role and text:
            return f'page.get_by_role("{inferred_role}", name="{self._escape_text(text)}")'
        
        # Priority 2: Label (for inputs)
        if tag == 'input' and 'label' in element_context:
            return f'page.get_by_label("{self._escape_text(element_context["label"])}")'
        
        # Priority 3: Placeholder
        if 'placeholder' in element_context:
            return f'page.get_by_placeholder("{self._escape_text(element_context["placeholder"])}")'
        
        # Check if trace locator has placeholder
        if locator_used and 'get_by_placeholder' in locator_used:
            return self._clean_locator(locator_used)
        
        # Priority 4: Text content
        if text:
            # For buttons and links, use exact text
            if tag in ['button', 'a', 'span'] and len(text) < 50:
                return f'page.get_by_text("{self._escape_text(text)}")'
        
        # Priority 5: Test ID
        if 'data-testid' in element_context:
            return f'page.get_by_test_id("{element_context["data-testid"]}")'
        
        # Priority 6: CSS fallback
        if locator_used:
            return self._convert_to_css_fallback(locator_used, tag, text)
        
        # Last resort: generic locator by tag and text
        if tag and text:
            return f'page.locator("{tag}").filter(has_text="{self._escape_text(text)}")'
        
        return 'page.locator("body")'  # Fallback
    
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
        
        # Special case: navigate action
        if action_type == 'navigate':
            if value:  # value contains target URL
                return f'page.goto("{value}")'
            return f'page.goto("{url}")'
        
        # Get template
        template = self.action_templates.get(action_type, '{locator}.click()')
        
        # Fill template
        code = template.format(
            locator=locator,
            value=value.replace('"', '\\"') if value else '',
            url=url
        )
        
        return code


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
                code.append(f'    {action_code}')
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
            return f'{var_name}.{locator_name}.click()'
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
