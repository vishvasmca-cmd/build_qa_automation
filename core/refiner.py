import json
import re
import os
import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

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
    2. **Smart Actions (MANDATORY)**: 
       - For every interaction (fill/click), you MUST use the `smart_action` function.
       - Syntax: `smart_action(page, """playwright_locator_string""", "action_type", value="optional_value")`
       - Example: `smart_action(page, """page.get_by_label('User')""", "fill", value="admin")`
       - **DO NOT** use `page.locator(...)` for interactive steps unless it's a composite locator.
       - **Composite Locators**: If 'element_context' is available, use it to create robust locators!
         - Ex: `smart_action(page, """page.locator('button.btn-primary', has_text='Start')""", "click")`
         - Ex: `smart_action(page, """page.locator('div.course-card').filter(has_text='AI').get_by_role('button')""", "click")`.
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
    
    **TRACE TO REFINE**:
    {trace_summary}
    """
    print(f"TRACE SUMMARY:\n{trace_summary}")
    
    print(f"TRACE SUMMARY:\n{trace_summary}")
    
    resp = llm.invoke(prompt)
    content = resp.content
    
    # 1. Strict Markdown Code Block Extraction
    import re
    code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
    if code_match:
        raw_steps = code_match.group(1).strip()
    else:
        # Fallback: Just try to use the whole content if no blocks
        raw_steps = content.strip()

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
            "if __name__"
        ]
        if any(item in line for item in blacklist): return False
        
        # Action calls and assertions are what we want
        valid_starters = ("smart_action", "expect(", "page.goto", "page.get_by", "page.locator", "take_screenshot")
        if any(line.startswith(s) for s in valid_starters): return True
        
        # Fallback for simple variable assignments
        if "=" in line and not line.startswith(" "): return True
        
        return False

    for line in lines:
        stripped = line.strip()
        # Remove 'await ' specifically from valid lines
        clean_line = line.replace("await ", "")
        
        if is_valid_step(clean_line):
             clean_lines.append(clean_line)
        else:
             print(f"   ✂️ Removing non-step line: {stripped}")
             
    clean_steps = textwrap.dedent("\n".join(clean_lines))
    
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
