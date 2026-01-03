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
        "url": t.get('url'),
        "action": t['action'],
        "locator": t.get('locator_used'),
        "value": t.get('value'),
        "reason": t.get('decision_reason'),
        "expectation": t.get('expected_outcome')
    } for t in trace], indent=2)
    
    base_url = next(iter(data.get("domain_info", {}).keys()), "the target website")

    prompt = f"""
    You are a Test Automation Engineer.
    Refine the trace into a linear Playwright script for {base_url}.
    
    **CRITICAL RULES**:
    1. **NO EXTERNAL URLS**: Your assertions MUST ONLY use the URL provided in the trace step's 'url' field. 
       - NEVER use 'academy.testifyltd.com' or any other URL not found in the trace.
       - If the trace step url is 'https://www.careerraah.com/blog', use THAT exactly.
    2. For interactive steps, use ONLY `smart_action(page, locator_string, "click"|"fill", value)`. 
       - locator_string MUST be the full `page.locator(...)` or `page.get_by_role(...)` string.
       - **CRITICAL**: Use the `locator` field from the trace VERBATIM. Do not try to "simplify" it. If the trace says `page.locator('a[href="/foo"]')`, use exactly that.
    3. After EVERY `smart_action`, call `take_screenshot(page, "step_N")` where N is the current step number.
    4. AddAssertions based on 'expectation' in step. Use `expect(page).to_have_url(...)` or `expect(page.locator("...")).to_have_value(...)` or `expect(page.locator("body")).to_contain_text(...)`.
       - **CRITICAL**: In assertions, the locator string MUST be clean. DO NOT add extra escaped quotes or brackets (e.g., NO `expect(page.locator("...\" )")`).
       - **CRITICAL**: In `expect(page).to_have_url(URL)`, the URL MUST be exactly the `url` field from the trace step. NEVER hallucinate or use external URLs.
    5. **RANDOMIZATION**: If trace fills a username/email, use the variable `username` or `email` instead of hardcoded value.
    5. **PYTHON RE-REQUIREMENT**: Use Python snake_case for methods (e.g., `get_by_role`, `get_by_text`).
    6. **NO JS OBJECTS**: For `get_by_role`, use: `page.get_by_role("button", name="Login")`. NEVER use JS-style `{{ name: 'Login' }}`.
    7. **PYTHON SYNTAX ONLY**: Do NOT use JavaScript syntax (e.g., NO `/regex/` literals). Use strings or `re.compile("...")`.
    8. **DANGER**: Do NOT output any imports, function definitions, or your own helper logic. 
    9. **DANGER**: Your output must consist ONLY of the code lines that go inside the `test_...` function.
    10. Ensure perfect 4-space indentation for every line of code.
    
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

    # 2. Filter out conversational lines (starting with alphabetic sentence)
    lines = raw_steps.split("\n")
    clean_lines = []
    
    # helper to check if a line is likely code
    def is_code(line):
        line = line.strip()
        if not line: return True
        if line.startswith("#"): return True
        # Logic words
        if line.startswith(("if ", "elif ", "else:", "for ", "while ", "try:", "except ", "with ", "def ", "class ")): return True
        # Action calls
        if "smart_action" in line or "take_screenshot" in line or "expect(" in line or "page." in line: return True
        # Variable assignment
        if "=" in line: return True
        return False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            clean_lines.append("")
            continue
            
        # Eliminate chatty lines "Okay, I will..."
        if not is_code(stripped) and len(stripped) > 0 and stripped[0].isalpha() and "=" not in stripped and "(" not in stripped:
             print(f"   ✂️ Removing chatty line: {stripped}")
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
        "import random",
        "from playwright.sync_api import Page, expect",
        "",
        "def wait_for_stability(page):",
        "    \"\"\"Ensures page is stable before interaction\"\"\"",
        "    try:",
        "        page.wait_for_load_state('domcontentloaded', timeout=5000)",
        "        page.wait_for_load_state('networkidle', timeout=3000)",
        "    except: pass",
        "    # Check for blocking overlays",
        "    page.evaluate(\"\"\"() => {",
        "        const overlays = document.querySelectorAll('.modal.show, .modal-backdrop.show, .overlay, [role=\"dialog\"]');",
        "        overlays.forEach(el => {",
        "             if (window.getComputedStyle(el).display !== 'none') {",
        "                 console.log('Found overlay, waiting/hiding:', el);",
        "                 // el.style.display = 'none'; // Optional: Aggressively hide if needed",
        "             }",
        "        });",
        "    }\"\"\")",
        "",
        "def smart_action(page, primary_locator, action_type, value=None):",
        "    \"\"\"Robust, Self-Healing Action Wrapper\"\"\"",
        "    wait_for_stability(page)",
        "    loc = None",
        "    try:",
        "        # 1. Parsing Locator",
        "        loc_str = primary_locator",
        "        import re",
        "        if 'page.' in loc_str:",
        "            loc_str = loc_str.replace('getByRole', 'get_by_role').replace('{ name:', 'name=').replace(' }', '')",
        "            match = re.search(r\"['\\\"](.*)['\\\"]\", loc_str)",
        "            if match and 'locator' in loc_str: loc_str = match.group(1)",
        "            if 'page.' in loc_str: loc = eval(loc_str, {'page': page, 're': re})",
        "        ",
        "        if not loc: loc = page.locator(loc_str)",
        "",
        "        # 2. Pre-Action Checks",
        "        if not loc.count() and 'strict mode' not in action_type:",
        "             # Try relaxed visibility",
        "             pass  ",
        "             ",
        "        # 3. Execution",
        "        if action_type == 'click':",
        "            try:",
        "                # Try normal Click",
        "                loc.click(timeout=5000)",
        "            except Exception as e:",
        "                print(f'⚠️ Standard click failed: {e}. Trying force.')",
        "                try:",
        "                    loc.click(timeout=3000, force=True)",
        "                except:",
        "                    # Last resort: JS Click",
        "                    print(f'☢️ JS Click needed for: {primary_locator}')",
        "                    loc.first.evaluate('el => el.click()')",
        "",
        "        elif action_type == 'fill':",
        "            loc.fill(str(value), timeout=5000)",
        "",
        "        return True",
        "",
        "    except Exception as e:",
        "        # 4. Self-Healing Fallback",
        "        print(f'🚑 Healing needed for: {primary_locator} ({e})')",
        "        try:",
        "            # Fallback 1: Text approximations",
        "            keyword = ''",
        "            match = re.search(r\"['\\\"](.*)['\\\"]\", primary_locator)",
        "            if match: keyword = match.group(1).lower()",
        "            ",
        "            # Find any button/link/input with similar text",
        "            if keyword:",
        "                healed = page.get_by_role('button', name=re.compile(keyword, re.IGNORECASE))",
        "                if healed.count():",
        "                     print('✨ Healed via Role/Name match!')",
        "                     if action_type == 'click': healed.first.click()",
        "                     else: healed.first.fill(str(value))",
        "                     return True",
        "        except: pass",
        "        ",
        "        print('❌ Action failed after healing attempts.')",
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
        "    timestamp = random.randint(1000, 9999)",
        "    username = f'user_{timestamp}'",
        "    email = f'test_{timestamp}@example.com'",
        "    page.context.set_default_timeout(60000)",
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
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding='utf-8') as f:
        f.write("\n".join(code))
    print(f"✅ Self-Healing Code Generated: {output_path}")

if __name__ == "__main__":
    import sys
    t_path = sys.argv[1] if len(sys.argv) > 1 else "explorer_trace.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "test_generated_from_trace.py"
    generate_code_from_trace(t_path, o_path)
