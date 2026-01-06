import json
import re
import os
import textwrap
import yaml
from dotenv import load_dotenv

import base64
from langchain_core.messages import HumanMessage, SystemMessage

# Import robust LLM wrapper
try:
    from .llm_utils import SafeLLM, try_parse_json
except (ImportError, ValueError):
    from llm_utils import SafeLLM, try_parse_json

# Import Metrics Logger
try:
    from .metrics_logger import logger
except ImportError:
    from metrics_logger import logger

def validate_python_syntax(code_string):
    """Check if generated Python code compiles without syntax errors."""
    import ast
    try:
        ast.parse(code_string)
        return True, None
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def find_undefined_variables(code_string):
    """Static analysis to find potentially undefined placeholder variables."""
    import ast
    try:
        tree = ast.parse(code_string)
        undefined = []
        defined_vars = {'page', 'expect', 'context', 'browser', 'pytest', 'os', 're', 'random'}
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id in ['locator', 'value', 'action_type'] and node.id not in defined_vars:
                    undefined.append(node.id)
        return list(set(undefined))
    except:
        return []

def validate_pom_scope(code_string):
    """Checks if 'page' is used instead of 'self.page' inside class methods (Sync with Reviewer)."""
    lines = code_string.split('\n')
    in_class = False
    errors = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('class '):
            in_class = True
            continue
        if in_class and stripped.startswith('def ') and not stripped.startswith('def test_'):
            # Basic POM methods check
            pass
        
        # Look for page.something() calls without self.
        if in_class and re.search(r"\bpage\.(get_by|locator|wait_for|goto|click|fill|select|expect)\(", line):
            if not re.search(r"self\.page\.", line):
                errors.append(f"Line {i+1}: Usage of 'page' inside class. Use 'self.page' instead.")
    
    return len(errors) == 0, "\n".join(errors)


class CodeRefiner:
    def __init__(self):
        load_dotenv()
        self.llm = SafeLLM(model="gemini-2.0-flash", temperature=0.0)

    def generate_code(self, target_url, trace_summary, images=None, error_context=None, domain="general"):
        """Generates cleaner, hardened code from a JSON trace summary, with optional visual, error, and domain context."""
        
        # Load Golden Examples
        golden_path = os.path.join(os.path.dirname(__file__), "training/golden_examples.json")
        golden_context = ""
        if os.path.exists(golden_path):
            try:
                with open(golden_path, "r", encoding="utf-8") as f:
                    examples = json.load(f)
                    golden_context = "\n**FEW-SHOT REFERENCE EXAMPLES (FOLLOW THESE PATTERNS)**:\n"
                    for ex in examples:
                        golden_context += f"- Pattern: {ex['pattern_name']}\n  Description: {ex['description']}\n  Ideal Code Implementation:\n```python\n{ex['ideal_code']}\n```\n"
            except: pass

        # Load Domain Rules
        domain_rules = ""
        domain_path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "domains", f"{domain}.yaml")
        if os.path.exists(domain_path):
            try:
                with open(domain_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    rules = data.get("learned_rules", [])
                    if rules:
                        domain_rules = "\n**DOMAIN-SPECIFIC LEARNED RULES (FOLLOW THESE)**:\n"
                        for r in rules:
                            domain_rules += f"- {r}\n"
            except: pass

        prompt_template = """
        You are an expert Playwright test automation engineer. 
        Refine the following execution trace into a linear, clean, and ROBUST Playwright script for {{TARGET_URL}}.
        
        {{GOLDEN_CONTEXT}}
        
        **PRIORITY ORDER (Always follow this sequence for locators)**:
        1. **USER-FACING LOCATORS** (Highest Priority):
           - `page.get_by_role()`: Select by ARIA roles and accessible names (e.g., `role="button", name="Submit"`)
           - `page.get_by_label()`: For form inputs with labels
           - `page.get_by_placeholder()`: For inputs with placeholder text
           - `page.get_by_text()`: For visible text content
           - `page.get_by_alt_text()`: For images
           - `page.get_by_title()`: For elements with title attributes
        2. **TEST-SPECIFIC LOCATORS**:
           - `page.get_by_test_id()`: Custom data-testid attributes
        3. **CSS SELECTORS** (Fallback only):
           - Use functional attributes over cosmetic ones. Keep selectors shallow and simple.
        4. **XPATH**: AVOID unless absolutely necessary.

        **COMPOSITE LOCATORS & FILTERING (CRITICAL)**:
        - **Chaining**: Chain locators to narrow scope: `page.get_by_role('listitem').filter(has_text='Product 2').get_by_role('button', name='Add to cart')`
        - **Multi-Level Filtering**: When nothing is unique, combine multiple non-unique characteristics:
          `page.locator('.notification').filter(has_text='Order #123').filter(has=page.locator('.status-active')).get_by_role('button', name='View')`
        - **Using .and_()**: Combine conditions: `page.get_by_role('button').and_(page.get_by_title('Subscribe'))`
        - **Contextual Anchoring**: Find a unique parent container first, then search within it.

        **MANDATORY: Page Object Model (POM) STRUCTURE**:
        You MUST generate a modular POM structure. This includes:
        1. **Page Object Classes**:
           - An `__init__` taking `page` and setting `self.page = page`.
           - **Property Locators**: Use `@property` for locators to ensure they are always fresh. 
             - Example: `return self.page.get_by_role("button", name="Login")`
           - **CRITICAL: Scope Integrity**: Inside class methods, you MUST use `self.page`. NEVER use a global `page` variable.
             - ✅ `self.page.wait_for_url("**/login")`
             - ❌ `page.wait_for_url("**/login")`  <-- THIS CAUSES NameError
           - **Action Methods**: Clean, reusable methods.
             - **CRITICAL**: When calling `smart_action` from a class method, pass the LOCATOR OBJECT directly, NOT a string.
             - ✅ `smart_action(self.page, self.username_field, "fill", value=username)`
             - ❌ `smart_action(self.page, "self.username_field", ...)`

        2. **Main Test Function**: A `test_autonomous_flow` function that follows the exact structure provided below.
           ```python
           def test_autonomous_flow(browser: Browser):
               # 1. Setup
               context = browser.new_context(viewport={"width": 1920, "height": 1080})
               page = context.new_page()
               page.goto("{{TARGET_URL}}")
               wait_for_stability(page)
               
               # 2. Logic (using POM)
               # ...
               
               # 3. Cleanup
               take_screenshot(page, "final_state", "{{PROJECT_NAME}}")
               context.close()
           ```

        {{DOMAIN_RULES}}

        **PROHIBITED PATTERNS (Anti-Hallucination)**:
        - ❌ NEVER use `page` inside a class method without `self.`.
        - ❌ NEVER use placeholder variables like `locator_string`, `action_type`, or `value` unless they are explicitly assigned from the trace.
        - ❌ NEVER redefine `smart_action`, `wait_for_stability`, or `take_screenshot`.
        - ❌ NEVER use positional `.nth(0)` if a text match or ID is available in the trace element context.

        **CRITICAL RULES**:
        1. **DO NOT REDEFINE HELPERS**: The following functions are ALREADY IMPORTED and available globally. **DO NOT** write code for them:
           - `smart_action(page, locator, action_type, value=None)`
           - `wait_for_stability(page)`
           - `take_screenshot(page, name, project_name)`
        2. **SYNC ONLY**: You MUST use SYNC Python Playwright. **DO NOT USE `await` keyword.**
        3. **PYTHON KWARGS ONLY**: 
           - ✅ `page.get_by_role("link", name="Home")`
           - **NEVER** use `{{ key: value }}` JS objects. Always use `key=value`.
        4. **Smart Actions (MANDATORY)**: Use `smart_action` for ALL interactions.
        5. **Navigation Guards**: ALWAYS call `wait_for_stability(page)` after every `smart_action`.
        6. **Visual Verification**: You are provided with screenshots of the elements. Use them to ensure your locators (roles/text) match what is visually present.
        
        **OUTPUT FORMAT**:
        You must output a JSON object with this EXACT structure:
        {
          "pages": [
            {
              "class_name": "LoginPage",
              "code": "class LoginPage:\\n    def __init__(self, page):... (full class code here)"
            }
          ],
          "test_logic": "def test_autonomous_flow(browser: Browser):\\n    # Setup, calls to POM actions, assertions, cleanup"
        }

        **TRACE TO REFINE**:
        {{TRACE_SUMMARY}}
        """
        
        if error_context:
            prompt_template += f"\n\n**IMPORTANT: PREVIOUS EXECUTION FAILED**:\n{error_context}\nPlease analyze the error and fix it in your new generation."
        prompt = prompt_template.replace("{{TARGET_URL}}", target_url)\
                               .replace("{{GOLDEN_CONTEXT}}", golden_context)\
                               .replace("{{TRACE_SUMMARY}}", trace_summary)\
                               .replace("{{PROJECT_NAME}}", os.path.basename(os.getcwd()))\
                               .replace("{{DOMAIN_RULES}}", domain_rules)

        # Prepare Multimodal Message
        content = [{"type": "text", "text": prompt}]
        if images:
            for img_b64 in images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                })
        
        # Layer 4: Retry Loop with Validation
        MAX_RETRIES = 2
        
        for attempt in range(MAX_RETRIES + 1):
            messages = [HumanMessage(content=content)]
            resp = self.llm.invoke(messages)
            
            result = try_parse_json(resp.content)
            if not result:
                if attempt < MAX_RETRIES:
                    content.append({"type": "text", "text": "Invalid JSON format. Please return ONLY the JSON object."})
                    continue
                else: 
                    return None

            # Validate generated pieces
            full_code = "\n\n".join([p["code"] for p in result.get("pages", [])]) + "\n\n" + result.get("test_logic", "")
            is_valid, syntax_error = validate_python_syntax(full_code)
            
            if is_valid:
                # Additional: POM Scope Check
                is_pom_valid, pom_error = validate_pom_scope(full_code)
                if is_pom_valid:
                    return full_code
                else:
                     if attempt < MAX_RETRIES:
                        content.append({"type": "text", "text": f"\n\n**POM SCOPE ERROR**:\n{pom_error}\n\nERROR: You used 'page' inside a class. You MUST use 'self.page'."})
                        continue
                     else:
                        return full_code # Return anyway on last try, maybe reviewer fixes it?
            
            if attempt < MAX_RETRIES:
                content.append({"type": "text", "text": f"\n\n**SYNTAX ERROR IN GENERATED CODE**:{syntax_error}\nFix this and ensure the code is valid Python."})
            else:
                return full_code
        
        return None

def generate_code_from_trace(trace_path="explorer_trace.json", output_path="test_generated_from_trace.py", workflow_goal="", error_context=None, domain="general"):
    if not os.path.exists(trace_path):
        print(f"❌ No trace found at {trace_path}")
        return

    with open(trace_path, "r") as f:
        data = json.load(f)

    trace = data.get("trace", [])
    target_url = data.get("target_url")
    if not target_url and trace:
        target_url = trace[0].get("url")
    if not target_url:
        target_url = "https://example.com"
    
    # SPECIAL CASE: Empty Trace + Goal = Direct Assertion Mode
    if not trace and workflow_goal:
        trace = [
            {"step": 1, "url": target_url, "action": "navigate", "locator_used": None},
            {"step": 2, "url": target_url, "action": "assert", "expected_outcome": workflow_goal}
        ]

    start_time = __import__('time').time()
    refiner = CodeRefiner()
    
    # Load Images for Multimodal Context
    images_b64 = []
    trace_dir = os.path.dirname(trace_path)
    for step in trace:
        img_name = step.get("screenshot")
        if img_name:
            img_path = os.path.join(trace_dir, img_name)
            if os.path.exists(img_path):
                try:
                    with open(img_path, "rb") as image_file:
                        images_b64.append(base64.b64encode(image_file.read()).decode('utf-8'))
                except: pass
    
    trace_summary = json.dumps([{
        "step": t['step'],
        "url": t.get('url'),
        "action": t['action'],
        "locator": t.get('locator_used') or t.get('locator'),
        "value": t.get('value'),
        "element_context": t.get('element_context'),
        "expectation": t.get('expected_outcome')
    } for t in trace], indent=2)
    
    raw_code = refiner.generate_code(target_url, trace_summary, images=images_b64, error_context=error_context, domain=domain)

    if not raw_code:
        print("❌ Refiner failed to generate valid code.")
        return False

    clean_steps = raw_code

    project_name = os.path.basename(os.path.dirname(os.path.dirname(trace_path)))
    
    from template_engine import TestTemplateEngine
    engine = TestTemplateEngine()
    final_code = engine.generate_test(
        project_name=project_name,
        target_url=target_url,
        test_steps=clean_steps
    )
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir): os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(final_code)
    print(f"✅ Self-Healing Code Generated: {output_path}")
    
    duration = __import__('time').time() - start_time
    logger.log_event("Refiner", "generate_code", duration, cost=0.01)

if __name__ == "__main__":
    import sys
    t_path = sys.argv[1] if len(sys.argv) > 1 else "explorer_trace.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "test_generated_from_trace.py"
    goal = sys.argv[3] if len(sys.argv) > 3 else ""
    e_path = sys.argv[4] if len(sys.argv) > 4 else None
    dom = sys.argv[5] if len(sys.argv) > 5 else "general"
    
    err_ctx = None
    if e_path and os.path.exists(e_path):
        with open(e_path, "r", encoding="utf-8", errors="ignore") as f:
            err_ctx = f.read()
            
    generate_code_from_trace(t_path, o_path, goal, error_context=err_ctx, domain=dom)
