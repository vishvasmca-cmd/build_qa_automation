"""
POM Template Engine - Generates Page Objects and Tests from structure
"""
import os
import json
from jinja2 import Template


class POMTemplateEngine:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
    def generate_from_structure(self, pom_structure_path, project_root):
        """
        Generate all Page Object files and tests from POM structure JSON
        
        Args:
            pom_structure_path: Path to pom_structure.json
            project_root: Root directory for the project (e.g., projects/careerraah_verification)
        """
        # Load POM structure
        with open(pom_structure_path, 'r', encoding='utf-8') as f:
            pom_data = json.load(f)
        
        # Create directories
        pages_dir = os.path.join(project_root, 'pages')
        tests_dir = os.path.join(project_root, 'tests', 'e2e')
        os.makedirs(pages_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)
        
        # Generate Page Objects
        page_files = []
        for page in pom_data['pages']:
            page_file = self._generate_page_object(page, pages_dir)
            page_files.append(page_file)
            print(f"✅ Generated: {page_file}")
        
        # Generate __init__.py for pages module
        init_file = os.path.join(pages_dir, '__init__.py')
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write('"""Page Objects for automated tests"""\n')
        print(f"✅ Generated: {init_file}")
        
        # Generate Test file
        test_file = self._generate_test_file(pom_data, tests_dir)
        print(f"✅ Generated: {test_file}")
        
        return {
            'pages': page_files,
            'tests': [test_file]
        }
    
    def _generate_page_object(self, page_data, output_dir):
        """Generate a single Page Object class file"""
        template_path = os.path.join(self.template_dir, 'page_object.py.jinja')
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        # Prepare template data
        template_data = {
            'page_name': page_data['name'],
            'page_url': page_data['url'],
            'locators': self._prepare_locators(page_data['locators']),
            'actions': self._prepare_actions(page_data['actions'])
        }
        
        # Render template
        rendered = template.render(**template_data)
        
        # Write to file
        filename = self._to_snake_case(page_data['name']) + '.py'
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        
        return output_path
    
    def _prepare_locators(self, locators):
        """Prepare locators for template"""
        prepared = []
        for loc in locators:
            prepared.append({
                'name': loc['name'],
                'selector': loc['selector'],
                'description': f"{loc['element'].get('tag', 'element')} - {loc['element'].get('text', 'no text')}"
            })
        return prepared
    
    def _prepare_actions(self, actions):
        """Prepare action methods for template"""
        prepared = []
        for action in actions:
            steps = []
            for step in action.get('steps', []):
                locator_name = step.get('locator_name', '')
                action_type = step.get('action', '')
                value = step.get('value')
                
                # Generate code for this step
                if action_type == 'fill':
                    # Use parameter variable name
                    param_var = locator_name.replace('_input', '')
                    code = f"self.{locator_name}.fill({param_var})"
                    comment = f"Fill {locator_name} with provided value"
                elif action_type == 'click':
                    code = f"self.{locator_name}.click()"
                    comment = f"Click {locator_name}"
                else:
                    code = f"self.{locator_name}.{action_type}()"
                    comment = f"{action_type.capitalize()} {locator_name}"
                
                steps.append({
                    'code': code,
                    'comment': comment
                })
            
            # Extract parameter descriptions
            params_list = action.get('params', '').split(', ') if action.get('params') else []
            param_descriptions = [f"{param.split(':')[0]}: {param.split(':')[1].strip()}" for param in params_list if param]
            
            prepared.append({
                'name': action['name'],
                'description': self._infer_action_description(action),
                'params': action.get('params', ''),
                'param_descriptions': param_descriptions,
                'steps': steps
            })
        
        return prepared
    
    def _infer_action_description(self, action):
        """Create description for action method"""
        name = action['name']
        if 'login' in name:
            return "Login to the application"
        elif 'click' in name:
            target = name.replace('click_', '').replace('_', ' ')
            return f"Click {target}"
        elif 'fill' in name:
            return "Fill in the form fields"
        else:
            return f"Perform {name.replace('_', ' ')}"
    
    def _generate_test_file(self, pom_data, output_dir):
        """Generate test file with all tests"""
        template_path = os.path.join(self.template_dir, 'test_pom.py.jinja')
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        # Prepare page imports
        page_imports = []
        for page in pom_data['pages']:
            page_imports.append({
                'module': self._to_snake_case(page['name']),
                'class_name': page['name']
            })
        
        # Render template
        rendered = template.render(
            base_url=pom_data['base_url'],
            page_imports=page_imports,
            tests=pom_data['tests']
        )
        
        # Write to file
        output_path = os.path.join(output_dir, 'test_main.py')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        
        return output_path
    
    def _to_snake_case(self, name):
        """Convert PascalCase to snake_case"""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pom_template_engine.py <pom_structure.json>")
        sys.exit(1)
    
    pom_structure_path = sys.argv[1]
    project_root = os.path.dirname(os.path.dirname(pom_structure_path))  # Go up from outputs/
    
    engine = POMTemplateEngine()
    result = engine.generate_from_structure(pom_structure_path, project_root)
    
    print(f"\n🎉 POM Generation Complete!")
    print(f"📁 Pages: {len(result['pages'])} files")
    print(f"📝 Tests: {len(result['tests'])} files")
