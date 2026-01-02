import json
import re
import os
import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

def generate_code_from_trace(trace_path="explorer_trace.json", output_path="test_generated_from_trace.py"):
    if not os.path.exists(trace_path):
        print(f"❌ No trace found at {trace_path}")
        return

    with open(trace_path, "r") as f:
        data = json.load(f)

    trace = data.get("trace", [])
    
    # Analyze Trace with LLM
    print(f"🧠 Refining Trace from {trace_path}...")
    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0)
    
    trace_summary = json.dumps([{
        "step": t['step'],
        "action": t['action'],
        "locator": t.get('locator_used'),
        "value": t.get('value'),
        "reason": t.get('decision_reason')
    } for t in trace], indent=2)
    
    prompt = f"""
    You are a Test Automation Engineer.
    Refine the trace into a linear Playwright script.
    
    **RULES**:
    1. For interactive steps, use ONLY `smart_action(page, locator_string, "click"|"fill", value)`. 
       - locator_string MUST be the full `page.locator(...)` or `page.get_by_role(...)` string.
    2. After EVERY `smart_action`, call `take_screenshot(page, "step_N")` where N is the current step number.
    3. Add standard Playwright `expect` assertions after key navigation/state changes.
    4. **PYTHON RE-REQUIREMENT**: Use Python snake_case for methods (e.g., `get_by_role`, `get_by_text`).
    5. **NO JS OBJECTS**: For `get_by_role`, use: `page.get_by_role("button", name="Login")`. NEVER use JS-style `{{ name: 'Login' }}`.
    6. **PYTHON SYNTAX ONLY**: Do NOT use JavaScript syntax (e.g., NO `/regex/` literals). Use strings or `re.compile("...")`.
    7. **DANGER**: Do NOT output any imports, function definitions, or your own helper logic. 
    8. **DANGER**: Your output must consist ONLY of the code lines that go inside the `test_...` function.
    9. Ensure perfect 4-space indentation for every line of code.
    
    **TRACE TO REFINE**:
    {trace_summary}
    """
    
    resp = llm.invoke(prompt)
    raw_steps = resp.content.replace("```python", "").replace("```", "").strip()
    
    # Severe filtering of LLM garbage
    lines = raw_steps.split("\n")
    clean_lines = []
    forbidden = ("import ", "from ", "def ", "class ", "if action ", "if locator ")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            clean_lines.append("")
            continue
        if stripped.startswith(forbidden):
            continue
        # If it looks like a function definition start, skip it
        if stripped.endswith(":"):
            # Check if it's a loop or valid control flow
            if stripped.startswith(("for ", "while ", "if ", "elif ", "else ", "try ", "except ")):
                pass
            else:
                continue
        clean_lines.append(line)
        
    clean_steps = textwrap.dedent("\n".join(clean_lines))
    
    # project_name = os.path.basename(os.path.dirname(os.path.dirname(output_path)))
    # Better: Derive from trace_path which is consistent (outputs/trace.json)
    project_name = os.path.basename(os.path.dirname(os.path.dirname(trace_path)))
    screenshot_dir = os.path.join("projects", project_name, "screenshots").replace("\\", "/")
    
    # Build complete test file
    code = [
        "import pytest",
        "import os",
        "import re",
        "from playwright.sync_api import Page, expect",
        "",
        "def smart_action(page, primary_locator, action_type, value=None):",
        "    \"\"\"Self-healing action wrapper\"\"\"",
        "    try:",
        "        # Clean the locator string if LLM passed page.locator(...) inside it",
        "        loc_str = primary_locator",
        "        import re",
        "        if 'page.' in loc_str:",
        "            # Convert JS getByRole to Python get_by_role with keyword args",
        "            loc_str = loc_str.replace('getByRole', 'get_by_role').replace('{ name:', 'name=').replace(' }', '')",
        "            match = re.search(r\"['\\\"](.*)['\\\"]\", loc_str)",
        "            if match and 'locator' in loc_str: loc_str = match.group(1)",
        "        ",
        "        # Final safeguard: if it still has page., try to eval it",
        "        if 'page.' in loc_str:",
        "             loc = eval(loc_str, {'page': page, 're': re})",
        "        else:",
        "             loc = page.locator(loc_str)",
        "        if action_type == 'click':",
        "            try:",
        "                loc.click(timeout=5000)",
        "            except Exception as e:",
        "                if \"strict mode\" in str(e):",
        "                    print(f'⚠️ Strict mode. Using .first for: {primary_locator}')",
        "                    loc.first.click(timeout=3000)",
        "                else:",
        "                    print(f'⚠️ Click failed. Trying force click for: {primary_locator}')",
        "                    try:",
        "                        loc.click(timeout=3000, force=True)",
        "                    except:",
        "                        print(f'☢️ Force failed. Trying JS Click for: {primary_locator}')",
        "                        loc.first.evaluate(\"el => el.click()\")",
        "",
        "        elif action_type == 'fill':",
        "            try:",
        "                loc.fill(str(value), timeout=5000)",
        "            except Exception as e:",
        "                if \"strict mode\" in str(e):",
        "                     loc.first.fill(str(value), timeout=3000)",
        "                else: raise e",
        "        return True",
        "    except Exception as e:",
        "        if \"strict mode\" in str(e):",
        "            try:",
        "                if action_type == 'click': loc.first.click(timeout=3000)",
        "                elif action_type == 'fill': loc.first.fill(str(value), timeout=3000)",
        "                print(f'⚠️ Strict mode handled for: {primary_locator}')",
        "                return True",
        "            except: pass",
        "        print(f'⚠️ Healing needed for: {primary_locator}')",
        "        all_elements = page.query_selector_all('[data-test], button, a, [role=\"button\"]')",
        "        # Try to find match by keyword",
        "        keyword = ''",
        "        import re",
        "        match = re.search(r\"['\\\"](.*)['\\\"]\", primary_locator)",
        "        if match: keyword = match.group(1).lower()",
        "        ",
        "        for el in all_elements:",
        "            attr = el.get_attribute('data-test') or el.get_attribute('id') or el.inner_text() or ''",
        "            if keyword and keyword in str(attr).lower():",
        "                try:",
        "                    print(f'✨ Healed! Found matching element.')",
        "                    if action_type == 'click': el.click()",
        "                    else: el.fill(str(value))",
        "                    return True",
        "                except: continue",
        "        print('❌ Healing failed.')",
        "        raise e",
        "",
        "def take_screenshot(page, name):",
        "    \"\"\"Consistent screenshot utility\"\"\"",
        f"    path = os.path.join('{screenshot_dir}', f'{{name}}.png')",
        "    os.makedirs(os.path.dirname(path), exist_ok=True)",
        "    page.screenshot(path=path)",
        "    print(f'📸 Saved: {path}')",
        "",
        "def test_autonomous_flow(page: Page):",
        f"    # Generated for {project_name}",
        f'    page.goto("{trace[0]["url"]}")' if trace else ""
    ]
    
    for line in clean_steps.split("\n"):
        if line.strip():
            # Force standard 1-level indent (4 spaces)
            code.append(f"    {line.lstrip().rstrip()}")
        else:
            code.append("")
            
    code.append(f'    take_screenshot(page, "final_state")')
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write("\n".join(code))
    print(f"✅ Self-Healing Code Generated: {output_path}")

if __name__ == "__main__":
    import sys
    t_path = sys.argv[1] if len(sys.argv) > 1 else "explorer_trace.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "test_generated_from_trace.py"
    generate_code_from_trace(t_path, o_path)
