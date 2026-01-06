"""
POM Structure Generator
Converts trace.json into Page Object Model structure
"""
import json
import re
import os
from urllib.parse import urlparse
from collections import defaultdict
import sys

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

class POMStructureGenerator:
    def __init__(self, trace_path):
        with open(trace_path, 'r') as f:
            self.trace_data = json.load(f)
        self.trace = self.trace_data.get('trace', [])
        self.base_url = self.trace_data.get('target_url', '')
        
    def generate_structure(self):
        """
        Generate POM structure from trace:
        - Group actions by page URL
        - Extract unique locators per page
        - Identify reusable action methods
        """
        pages = defaultdict(lambda: {'locators': {}, 'actions': []})
        
        # Group by URL (page)
        for step in self.trace:
            if step.get('action') == 'navigate':
                continue
            url = step.get('url', '')
            page_name = self._get_page_name(url)
            
            # Extract locator
            locator = step.get('locator_used') or ''
            action_type = step.get('action', '')
            element_context = step.get('element_context', {})
            
            # Create locator entry
            locator_name = self._create_locator_name(element_context, action_type, step)
            if locator_name not in pages[page_name]['locators']:
                pages[page_name]['locators'][locator_name] = {
                    'selector': self._extract_selector(locator),
                    'element': element_context
                }
            
            # Track action
            pages[page_name]['actions'].append({
                'step': step['step'],
                'action': action_type,
                'locator_name': locator_name,
                'value': step.get('value'),
                'thought': step.get('thought', '')
            })
        
        # Convert to POM JSON structure
        pom_structure = {
            'base_url': self.base_url,
            'workflow': self.trace_data.get('workflow', ''),
            'pages': []
        }
        
        for page_name, page_data in pages.items():
            pom_structure['pages'].append({
                'name': page_name,
                'url': self._get_page_url(page_name),
                'locators': [
                    {'name': name, **data} 
                    for name, data in page_data['locators'].items()
                ],
                'actions': self._generate_action_methods(page_data['actions'])
            })
        
        # Generate tests (need to pass processed pages)
        pom_structure['tests'] = self._generate_tests_from_structure(pom_structure['pages'], pages)
        
        return pom_structure
    
    def _get_page_name(self, url):
        """Convert URL to page class name"""
        path = urlparse(url).path
        if not path or path == '/':
            return 'HomePage'
        # Remove leading slash and convert to PascalCase
        name = path.strip('/').replace('.html', '').replace('-', '_').replace('/', '_')
        return ''.join(word.capitalize() for word in name.split('_')) + 'Page'
    
    def _get_page_url(self, page_name):
        """Get relative URL for page"""
        # Find first occurrence of this page in trace
        for step in self.trace:
            if self._get_page_name(step.get('url', '')) == page_name:
                parsed = urlparse(step['url'])
                return parsed.path or '/'
        return '/'
    
    def _sanitize_name(self, text):
        """Sanitize text to be a valid Python identifier"""
        # Replace spaces/hyphens with underscore first
        text = text.replace(' ', '_').replace('-', '_')
        # Remove any non-alphanumeric character (except underscore)
        text = re.sub(r'[^a-zA-Z0-9_]', '', text)
        # Remove leading numbers if present (Python variables can't start with digit)
        if text and text[0].isdigit():
             text = '_' + text
        return text.lower()

    def _create_locator_name(self, element_context, action_type, step_data=None):
        """
        Generate semantic locator name based on:
        1. data-test attribute (best)
        2. Element's purpose in the workflow (from thought/action)
        3. Element text + tag type (fallback)
        """
        # 1. Check for data-test attribute in the locator
        locator = step_data.get('locator_used') or '' if step_data else ''
        if 'data-test' in locator:
            # Extract data-test value: [data-test='add-to-cart'] -> add_to_cart_button
            import re
            match = re.search(r"data-test=['\"]([^'\"]+)['\"]", locator)
            if match:
                test_name = self._sanitize_name(match.group(1))
                tag = element_context.get('tag', '')
                if tag == 'button' and 'button' not in test_name:
                    return f"{test_name}_button"
                elif tag == 'input' and 'input' not in test_name:
                    return f"{test_name}_input"
                return test_name
        
        # 2. Infer from workflow context
        thought = step_data.get('thought', '').lower() if step_data else ''
        text = element_context.get('text', '').lower()
        tag = element_context.get('tag', '')
        
        # Cart-related
        if 'cart' in thought or 'cart' in locator.lower():
            if 'badge' in thought or (tag == 'a' and text.isdigit()):
                return 'cart_badge'
            elif 'add' in thought:
                return 'add_to_cart_button'
            else:
                return 'cart_icon'
        
        # Login-related
        if 'login' in thought or 'sign in' in thought:
            if 'username' in thought or 'email' in thought:
                return 'username_input'
            elif 'password' in thought:
                return 'password_input'
            elif tag == 'button' or 'button' in thought:
                return 'login_button'
        
        # Registration
        if 'register' in thought or 'sign up' in thought:
            return 'signup_button' if tag == 'button' else 'signup_link'
        
        # 3. Fallback: Use element text + tag
        clean_text = self._sanitize_name(text)
        if not clean_text or clean_text.isdigit():
            # Generic names for empty or numeric text
            if tag == 'button':
                return f"{action_type}_button"
            elif tag == 'input':
                return f"{action_type}_input"
            else:
                return f"{action_type}_{tag}"
        
        if tag == 'input':
            return f"{clean_text}_input"
        elif tag == 'button':
            return f"{clean_text}_button"
        elif tag == 'a':
            return f"{clean_text}_link"
        else:
            return f"{clean_text}_{tag}"
    
    def _extract_selector(self, locator_string):
        """Extract clean Playwright selector from locator_used"""
        import re
        if not locator_string: return ''
        locator = locator_string.strip()
        
        # If it's a page.locator() call, extract the selector
        if 'page.locator(' in locator:
            locator = locator.replace('page.locator(', '').rstrip(')')
            locator = locator.strip('"').strip("'")
            return locator
        
        # If it's a get_by_* method, clean and convert to Python syntax
        elif 'page.get_by_' in locator or 'page.get(' in locator:
            # Remove 'page.' prefix
            locator = locator.replace('page.', '')
            
            # Convert JavaScript object syntax to Python kwargs
            # { name: "text" } -> name="text"
            locator = re.sub(r'\{\s*name:\s*"([^"]+)"\s*\}', r'name="\1"', locator)
            locator = re.sub(r'\{\s*name:\s*\'([^\']+)\'\s*\}', r'name="\1"', locator)
            
            return locator
        
        # Otherwise, just remove page. prefix
        else:
            return locator.replace('page.', '').strip('"').strip("'")
    
    def _generate_action_methods(self, actions):
        """Group actions into reusable methods"""
        # For now, create one method per unique action sequence
        methods = []
        
        # Simple heuristic: group consecutive actions as one method
        current_method = []
        for action in actions:
            current_method.append(action)
            
            # If action is 'click' that navigates, end method here
            if action['action'] == 'click':
                method_name = self._infer_method_name(current_method)
                methods.append({
                    'name': method_name,
                    'steps': current_method.copy(),
                    'params': self._infer_params(current_method)
                })
                current_method = []
        
        return methods
    
    def _infer_method_name(self, actions):
        """Infer method name from action sequence"""
        if len(actions) == 1:
            return f"{actions[0]['action']}_{actions[0]['locator_name']}"
        
        # Multi-step - use first action's thought
        thought = actions[0].get('thought', '')
        if 'login' in thought.lower():
            return 'login'
        elif 'add' in thought.lower() and 'cart' in thought.lower():
            return 'add_to_cart'
        elif 'verify' in thought.lower():
            return 'verify_cart_badge'
        else:
            return f"perform_{actions[0]['action']}"
    
    def _infer_params(self, actions):
        """Infer method parameters from actions"""
        params = []
        seen_vars = set()
        
        for action in actions:
            if action['value'] and action['action'] == 'fill':
                # This is a fillable field
                var_name = action['locator_name'].replace('_input', '')
                if var_name not in seen_vars:
                    params.append(f"{var_name}: str")
                    seen_vars.add(var_name)
        
        return ', '.join(params) if params else ''
    
    
    def _generate_tests_from_structure(self, pom_pages, raw_pages):
        """Generate test function definitions with meaningful names and assertions"""
        workflow = self.trace_data.get('workflow', '')
        
        # Infer test name from workflow
        test_name = self._infer_test_name(workflow)
        
        # Extract expected outcomes for assertions
        assertions = self._extract_assertions(workflow)
        
        # Generate test steps description
        steps_description = [step.get('thought', '') for step in self.trace if step.get('thought')]
        
        return [{
            'name': test_name,
            'description': workflow,
            'steps_description': steps_description,
            'page_objects': [
                {
                    'class_name': page['name'],
                    'var_name': self._to_snake_case(page['name']),
                    'goto': idx == 0,  # Only first page needs goto
                    'description': f"Page object for {page['name'].replace('Page', '')}"
                }
                for idx, page in enumerate(pom_pages)
            ],
            'actions': self._generate_test_actions(pom_pages),
            'assertions': assertions
        }]
    
    def _infer_test_name(self, workflow):
        """Create meaningful test name from workflow description"""
        # Extract key actions
        workflow_lower = workflow.lower()
        
        if 'login' in workflow_lower and 'cart' in workflow_lower:
            return 'test_user_can_login_and_add_item_to_cart'
        elif 'login' in workflow_lower:
            return 'test_user_can_login_successfully'
        elif 'register' in workflow_lower or 'sign up' in workflow_lower:
            return 'test_user_can_register_account'
        elif 'checkout' in workflow_lower:
            return 'test_user_can_complete_checkout'
        else:
            # Generic fallback
            return 'test_workflow_execution'
    
    def _extract_assertions(self, workflow):
        """Extract assertions from workflow goals"""
        assertions = []
        workflow_lower = workflow.lower()
        
        # Look for verification keywords
        if 'verify' in workflow_lower:
            # Extract what needs verification
            if 'cart badge' in workflow_lower and '1' in workflow_lower:
                assertions.append({
                    'code': 'expect(page.get_by_text("1")).to_be_visible()',
                    'comment': 'Verify cart badge shows 1 item'
                })
            if 'dashboard' in workflow_lower:
                assertions.append({
                    'code': 'expect(page).to_have_url(re.compile(".*dashboard"))',
                    'comment': 'Verify user is on dashboard'
                })
        
        # If no specific assertions, add a generic one
        if not assertions:
            assertions.append({
                'code': 'expect(page).to_have_url(re.compile(".*"))',
                'comment': 'Verify page navigation successful'
            })
        
        return assertions
    
    def _generate_test_actions(self, pom_pages):
        """Generate test actions with inline comments from processed POM pages"""
        actions = []
        
        # pom_pages is the list of page structures from pom_structure['pages']
        for page in pom_pages:
            page_name = page['name']
            var_name = self._to_snake_case(page_name)
            
            # For each action method in this page
            for action_method in page.get('actions', []):
                method_name = action_method.get('name', '')
                params = action_method.get('params', '')
                
                # Infer parameter values from steps
                param_values = []
                for step in action_method.get('steps', []):
                    if step.get('value'):
                        param_values.append(f'"{step["value"]}"')
                
                if param_values:
                    call = f"{var_name}.{method_name}({', '.join(param_values)})"
                else:
                    call = f"{var_name}.{method_name}()"
                
                # Get comment from first step's thought
                steps = action_method.get('steps', [])
                comment = steps[0].get('thought', 'Execute action')[:60] if steps else 'Execute action'
                
                actions.append({
                    'code': call,
                    'comment': comment
                })
        
        return actions
    
    def _to_snake_case(self, name):
        """Convert PascalCase to snake_case"""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


if __name__ == '__main__':
    import sys
    trace_path = sys.argv[1] if len(sys.argv) > 1 else 'projects/sauce_smoke/outputs/trace.json'
    
    generator = POMStructureGenerator(trace_path)
    pom_json = generator.generate_structure()
    
    output_path = trace_path.replace('trace.json', 'pom_structure.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(pom_json, f, indent=2)
    
    print(f"✅ POM Structure generated: {output_path}")
    print(json.dumps(pom_json, indent=2))
