import json
import re
import os
import textwrap
from dotenv import load_dotenv

# Import robust LLM wrapper
try:
    from .llm_utils import SafeLLM
except (ImportError, ValueError):
    from llm_utils import SafeLLM

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

class CodeRefiner:
    def __init__(self):
        load_dotenv()
        self.llm = SafeLLM(model="gemini-2.0-flash", temperature=0.0)

    def generate_code(self, target_url, trace_summary):
        """Generates cleaner, hardened code from a JSON trace summary."""
        
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

        **CRITICAL RULES**:
        1. **SYNC ONLY**: You MUST use SYNC Python Playwright. **DO NOT USE `await` keyword.**
        2. **PYTHON KWARGS ONLY**: 
           - ✅ `page.get_by_role("link", name="Home")`
           - **NEVER** use `{{ key: value }}` JS objects. Always use `key=value`.
        3. **Smart Actions (MANDATORY)**: 
           - For every interaction (fill/click), you MUST use the `smart_action` function.
           - Syntax: `smart_action(page, "playwright_locator_string", "action_type", value="optional_value")`
           - **DO NOT** use brittle CSS like `div.container > section > button` if semantic locators can be chained.
        4. **Navigation Guards**: ALWAYS call `wait_for_stability(page)` after every `smart_action`.
        5. **NO TEMPLATE LOGIC**: Use only concrete locators and values from the trace JSON below.
        
        **TRACE TO REFINE**:
        {{TRACE_SUMMARY}}
        """
        prompt = prompt_template.replace("{{TARGET_URL}}", target_url)\
                              .replace("{{GOLDEN_CONTEXT}}", golden_context)\
                              .replace("{{TRACE_SUMMARY}}", trace_summary)

        # Layer 4: Retry Loop with Validation
        MAX_RETRIES = 2
        raw_steps = None
        
        for attempt in range(MAX_RETRIES + 1):
            resp = self.llm.invoke(prompt)
            content = resp.content
            
            code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
            candidate_code = code_match.group(1).strip() if code_match else content.strip()
            
            is_valid, syntax_error = validate_python_syntax(candidate_code)
            undefined_vars = find_undefined_variables(candidate_code)
            
            if is_valid and not undefined_vars:
                raw_steps = candidate_code
                break
            
            if attempt < MAX_RETRIES:
                error_context = ""
                if not is_valid: error_context += f"\n**SYNTAX ERROR**: {syntax_error}\n"
                if undefined_vars: error_context += f"\n**UNDEFINED VARIABLES**: {', '.join(undefined_vars)}\n"
                prompt += f"\n\n**YOUR PREVIOUS ATTEMPT HAD ERRORS**:{error_context}\nFix these. Use ONLY concrete values."
            else:
                raw_steps = candidate_code
        
        return raw_steps

def generate_code_from_trace(trace_path="explorer_trace.json", output_path="test_generated_from_trace.py", workflow_goal=""):
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
    
    trace_summary = json.dumps([{
        "step": t['step'],
        "url": t.get('url'),
        "action": t['action'],
        "locator": t.get('locator_used') or t.get('locator'),
        "value": t.get('value'),
        "element_context": t.get('element_context'),
        "expectation": t.get('expected_outcome')
    } for t in trace], indent=2)
    
    raw_steps = refiner.generate_code(target_url, trace_summary)

    # Filter out conversational lines
    clean_lines = []
    def is_valid_step(line):
        line = line.strip()
        if not line:
            return True
        if line.startswith("#"):
            return True
        # Allow chaining and filtering constructs
        if ".filter(" in line or ".and_" in line:
            return True
        blacklist = ["playwright.chromium", "browser =", "context =", "new_page", "sync_playwright", "with ", "context.close", "browser.close"]
        if any(item in line for item in blacklist):
            return False
        # Check for undefined variables
        if any(p in line for p in ['locator_string', 'optional_value', 'action_type']):
            return False
        if re.search(r"\.locator\s*\(\s*locator\s*[\),]", line):
            return False
        valid_starters = ("smart_action", "expect(", "page.goto", "page.get_by", "page.locator", "take_screenshot", "wait_for_stability", "if ", "for ", "print(")
        return any(line.startswith(s) for s in valid_starters) or ("=" in line)

    for line in raw_steps.split("\n"):
        clean_line = line.replace("await ", "").strip()
        if is_valid_step(clean_line):
             # Maintain relative indentation for control flow
             original_indent = len(line) - len(line.lstrip())
             clean_lines.append("        " + (" " * original_indent) + clean_line)
             
    clean_steps = "\n".join(clean_lines)
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
    generate_code_from_trace(t_path, o_path, goal)
