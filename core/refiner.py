import json
import re
import os
import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def validate_python_syntax(code_string):
    """
    Check if generated Python code compiles without syntax errors.
    Returns: (is_valid: bool, error_message: str or None)
    """
    import ast
    try:
        ast.parse(code_string)
        return True, None
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def find_undefined_variables(code_string):
    """
    Static analysis to find potentially undefined placeholder variables.
    Returns: list of suspicious variable names
    """
    import ast
    try:
        tree = ast.parse(code_string)
        undefined = []
        
        # Known variables that should exist in test context
        defined_vars = {'page', 'expect', 'context', 'browser', 'pytest', 'os', 're', 'random'}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                # Check for common placeholder variable names
                if node.id in ['locator', 'value', 'action_type'] and node.id not in defined_vars:
                    undefined.append(node.id)
        
        return list(set(undefined))
    except:
        return []

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
        print(f"⚠️ Empty trace detected. Generating assertions based on Goal: '{workflow_goal}'")
        trace = [
            {"step": 1, "url": target_url, "action": "navigate", "locator_used": None, "decision_reason": "Navigate to target"},
            {"step": 2, "url": target_url, "action": "assert", "locator_used": "PROPOSE_BEST_LOCATOR", "decision_reason": f"Verify user goal: {workflow_goal}", "expected_outcome": workflow_goal}
        ]

    # Analyze Trace with LLM
    print(f"🧠 Refining Trace from {trace_path}...")
    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0)
    
    trace_summary = json.dumps([{
        "step": t['step'],
        "url": t.get('url'),
        "action": t['action'],
        "locator": t.get('locator_used') or t.get('locator'),
        "value": t.get('value'),
        "element_context": t.get('element_context'), # Pass rich context to LLM
        "reason": t.get('decision_reason'),
        "expectation": t.get('expected_outcome')
    } for t in trace], indent=2)
    
    base_url = target_url
    
    # Load Golden Examples for Few-Shot Learning
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

    prompt = f"""
    You are a Test Automation Engineer.
    Refine the following execution trace into a linear, clean Playwright script for {target_url}.
    
    {golden_context}
    
    **CRITICAL RULES**:
    1. **SYNC ONLY**: You MUST use SYNC Python Playwright. **DO NOT USE `await` keyword.**
    2. **PYTHON KWARGS ONLY**: 
       - ❌ **WRONG (messes up Python)**: `page.get_by_role("link", {{ name: "Home" }})`
       - ✅ **RIGHT (Pythonic)**: `page.get_by_role("link", name="Home")`
       - **NEVER** use `{{ key: value }}` JS objects inside Python function calls. Always use `key=value`.
    3. **Smart Actions (MANDATORY)**: 
       - For every interaction (fill/click), you MUST use the `smart_action` function.
       - Syntax: `smart_action(page, \"\"\"playwright_locator_string\"\"\", \"action_type\", value=\"optional_value\")`
       - Example: `smart_action(page, \"\"\"page.get_by_label('User')\"\"\", \"fill\", value=\"admin\")`
       - **DO NOT** use `page.locator(...)` for interactive steps unless it's a composite locator.
       - **Composite Locators**: If 'element_context' is available, use it to create robust locators!
         - **Prioritize Unique IDs**: Always prefer `data-test`, `id`, or `name` if available in context.
         - **Hierarchy**: Use hierarchy to avoid Stick Mode errors: `smart_action(page, \"\"\"page.get_by_role('form').get_by_placeholder('Name')\"\"\", \"fill\")`
         - Ex: `smart_action(page, \"\"\"page.locator('button.btn-primary', has_text='Start')\"\"\", \"click\")`
         - Ex: `smart_action(page, \"\"\"page.locator('div.course-card').filter(has_text='AI').get_by_role('button')\"\"\", \"click\")`
       - **DO NOT** use `page.locator(...)` for simple interactions if `smart_action` is safer.
    3. **Indentation**: 
       - Use exactly 4 spaces for indentation.
    4. **Condense Steps**: 
       - If the trace shows redundant clicks or loops, output only the successful final interaction.
    5. **Hardened Control Flow (MANDATORY)**:
       - **Iterative Stability**: If the goal involves lists (courses, posts), REQUIRE index-based loops (`nth(i)`).
       - **Navigation Guards**: ALWAYS call `wait_for_stability(page)` after every `smart_action`.
       - **URL Verification**: Use `page.wait_for_url` after significant navigation clicks.
    6. **Navigation**: 
       - Use `page.goto("{target_url}")` at the start.
    7. **NO TEMPLATE LOGIC**: 
       - DO NOT include generic `if action == 'click':` blocks.
       - DO NOT use placeholder variables like `locator`, `value`, or `action_type`.
       - Use only the CONCRETE values provided in the TRACE.
    
    **CRITICAL: AVOID THESE PATTERNS** (Common LLM Mistakes):
    ❌ WRONG: `page.locator(locator).click()`  # 'locator' variable undefined!
    ❌ WRONG: `page.locator(locator).fill(value)`  # 'value' variable undefined!
    ❌ WRONG: `if action_type == "click": page.locator(loc).click()`  # Generic conditionals
    
    ✅ RIGHT: `smart_action(page, \"\"\"page.locator("#signin2")\"\"\", "click")`
    ✅ RIGHT: `smart_action(page, \"\"\"page.get_by_placeholder("Email")\"\"\", "fill", value="test@example.com")`
    ✅ RIGHT: Use ONLY concrete locators and values from the trace JSON above.
    
    **TRACE TO REFINE**:
    {trace_summary}
    """
    print(f"TRACE SUMMARY:\n{trace_summary}")
    
    # Layer 4: Retry Loop with Validation
    MAX_RETRIES = 2
    raw_steps = None
    
    for attempt in range(MAX_RETRIES + 1):
        print(f"\n🔄 Attempt {attempt + 1}/{MAX_RETRIES + 1}...")
        
        resp = llm.invoke(prompt)
        content = resp.content
        
        # 1. Extract code from markdown
        code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
        if code_match:
            candidate_code = code_match.group(1).strip()
        else:
            candidate_code = content.strip()
        
        # 2. Validate before processing
        is_valid, syntax_error = validate_python_syntax(candidate_code)
        undefined_vars = find_undefined_variables(candidate_code)
        
        if is_valid and not undefined_vars:
            print(f"✅ Code validated successfully on attempt {attempt + 1}")
            raw_steps = candidate_code
            break
        
        # If validation failed and we have retries left
        if attempt < MAX_RETRIES:
            error_context = ""
            if not is_valid:
                error_context += f"\n**SYNTAX ERROR**: {syntax_error}\n"
            if undefined_vars:
                error_context += f"\n**UNDEFINED VARIABLES**: {', '.join(undefined_vars)} - NOT defined!\n"
            
            print(f"⚠️ Validation failed:{error_context.strip()}")
            print(f"   Retrying with error feedback...")
            
            # Append error feedback for next attempt
            prompt += f"\n\n**YOUR PREVIOUS ATTEMPT HAD ERRORS**:{error_context}"
            prompt += "\nFix these. Use ONLY concrete values from the trace."
        else:
            print(f"❌ Max retries reached. Using last generation.")
            raw_steps = candidate_code
    
    if not raw_steps:
        raw_steps = candidate_code

    # 2. Filter out conversational lines and setup code
    lines = raw_steps.split("\n")
    clean_lines = []
    
    # helper to check if a line is likely code we want to keep
    def is_valid_step(line):
        line = line.strip()
        if not line: return True
        if line.startswith("#"): return True
        
        # Blacklist setup/boilerplate lines
        blacklist = [
            "playwright.chromium", "browser =", "context =", "new_page", 
            "sync_playwright", "with ", "def ", "return ", "async ", 
            "await ", "context.close", "browser.close", "Args:", "page:",
            "locator:", "value:", "type:", "Returns:", "if action_type",
            "if __name__", "screenshots/" 
        ]
        if any(item in line for item in blacklist): return False
        
        # Blacklist garbage placeholders from LLM
        def has_undefined_variables(line):
            """Detect common LLM placeholder patterns that indicate undefined variables."""
            import re
            
            # Pattern 1: page.locator(locator) - bare variable
            if re.search(r'\.locator\s*\(\s*locator\s*[\),]', line):
                return True
            
            # Pattern 2: .fill(value) or .type(value) - bare variable (not string)
            if re.search(r'\.(fill|type)\s*\(\s*value\s*[\),]', line):
                return True
            
            # Pattern 3: Generic action_type conditionals
            if 'action_type' in line or 'if action ==' in line:
                return True
            
            # Pattern 4: Placeholder strings
            if any(p in line for p in ['locator_string', 'optional_value']):
                return True
            
            return False
        
        if has_undefined_variables(line):
            print(f"   🚫 Rejected: Undefined variable pattern")
            return False
        
        # Action calls and assertions are what we want
        valid_starters = ("smart_action", "expect(", "page.goto", "page.get_by", "page.locator", "take_screenshot", "wait_for_stability")
        if any(line.startswith(s) for s in valid_starters): return True
        
        # Fallback for simple variable assignments
        if "=" in line and not line.startswith(" "): return True
        
        return False

    for line in lines:
        stripped = line.strip()
        # Remove 'await ' specifically from valid lines
        clean_line = line.replace("await ", "").strip()
        
        if is_valid_step(clean_line):
             # Force 8 spaces indentation for try-block inside test function
             indented_line = "        " + clean_line
             clean_lines.append(indented_line)
        else:
             print(f"   ✂️ Removing non-step line: {stripped}")
             
    clean_steps = "\n".join(clean_lines)
    
    # project_name = os.path.basename(os.path.dirname(os.path.dirname(output_path)))
    # Better: Derive from trace_path which is consistent (outputs/trace.json)
    project_name = os.path.basename(os.path.dirname(os.path.dirname(trace_path)))
    screenshot_dir = os.path.join("projects", project_name, "screenshots").replace("\\", "/")
    
    
    # ============================================
    # NEW: Use Template Engine (No more f-string hell!)
    # ============================================
    from template_engine import TestTemplateEngine
    
    engine = TestTemplateEngine()
    final_code = engine.generate_test(
        project_name=project_name,
        target_url=target_url,
        test_steps=clean_steps
    )
    
    
    # Write to file
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(final_code)
    print(f"✅ Self-Healing Code Generated: {output_path}")

if __name__ == "__main__":
    import sys
    t_path = sys.argv[1] if len(sys.argv) > 1 else "explorer_trace.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "test_generated_from_trace.py"
    goal = sys.argv[3] if len(sys.argv) > 3 else ""
    generate_code_from_trace(t_path, o_path, goal)
