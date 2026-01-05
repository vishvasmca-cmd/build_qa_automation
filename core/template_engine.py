"""
Template Engine for Test Generation
Loads pre-tested templates and merges with LLM-generated steps
"""
import os
from jinja2 import Template


class TestTemplateEngine:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
    def generate_test(self, project_name, target_url, test_steps):
        """
        Generate final test file from template + LLM steps
        
        Args:
            project_name: Name of the project
            target_url: Starting URL
            test_steps: Python code string with test steps (from LLM)
        
        Returns:
            Complete test file content as string
        """
        # Load template
        template_path = os.path.join(self.template_dir, 'test_base.py.jinja')
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        # Render with data
        helpers_path = os.path.abspath(self.template_dir).replace("\\", "/")
        
        rendered = template.render(
            project_name=project_name,
            target_url=target_url,
            test_steps=test_steps,
            helpers_path=helpers_path
        )
        
        return rendered


if __name__ == "__main__":
    # Test the engine
    engine = TestTemplateEngine()
    sample_steps = """
    smart_action(page, "[data-test='username']", "fill", value="standard_user")
    wait_for_stability(page)
    smart_action(page, "[data-test='password']", "fill", value="secret_sauce")
    wait_for_stability(page)
    smart_action(page, "[data-test='login-button']", "click")
    wait_for_stability(page)
    """
    
    result = engine.generate_test("sauce_smoke", "https://www.saucedemo.com/", sample_steps)
    print(result)
