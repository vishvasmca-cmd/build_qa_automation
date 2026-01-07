import sys

# Windows Unicode Fix
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import os
import sys
import io
import json
import re
import yaml
from dotenv import load_dotenv

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    pass # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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

class CodeReviewer:
    def __init__(self):
        load_dotenv()
        # Use JSON mode for structural reliability
        self.llm = SafeLLM(
            model="gemini-2.0-flash", 
            temperature=0.1
        )

    def _try_parse_json(self, content):
        """Attempts to parse JSON even with markdown wrapping or common errors."""
        cleaned = content.strip()
        # 1. Strip Markdown
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            # 2. Lenient Recovery
            import re
            print(f"⚠️ JSON Parse Error: {e}. Attempting recovery...")
            try:
                # Heuristic: Fix unescaped newlines and problematic backslashes inside JSON string values
                # This only targets content between : " and the next "
                def _fix_value(match):
                    val = match.group(1)
                    val = val.replace('\n', '\\n')   # Unescaped newlines
                    # Escape backslashes that aren't already part of a valid escape
                    # (Quick & dirty: just double all backslashes that aren't already doubled)
                    val = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', val)
                    return val

                cleaned_alt = re.sub(r'(?<=: ")(.*?)(?=")', _fix_value, cleaned, flags=re.DOTALL)
                return json.loads(cleaned_alt)
            except:
                # 3. Final Fallback: Regex extraction for the 'final_code' field if everything else fails
                code_match = re.search(r'"final_code":\s*"(.*)"\s*}', cleaned, re.DOTALL)
                if code_match:
                    code = code_match.group(1).replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
                    return {"status": "FIXED", "final_code": code, "review_summary": "Recovered via regex."}
            return None

    def _validate_pom_scope(self, code):
        """Checks if 'page' is used instead of 'self.page' inside class methods."""
        lines = code.split('\n')
        in_class = False
        in_init = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            if line.startswith('class '):
                in_class = True
                continue
            
            # Simple method detection (flaky but consistent with previous logic)
            if in_class and stripped.startswith('def '):
                if '__init__' in line:
                    in_init = True
                else:
                    in_init = False
            
            # Skip scope check for __init__ methods where 'page' arg is valid
            if in_init:
                continue
            
            if in_class and line.startswith('def ') and not stripped.startswith('def test_'):
                # Top level def (not test) ends class? Not really, but keeping legacy logic
                pass 
            
            if in_class and re.search(r"\bpage\.(get_by|locator|wait_for|goto|click|fill|select)\(", line):
                # Check if it's NOT self.page
                if not re.search(r"self\.page\.", line):
                    return False, f"POM Scope Violation at line {i+1}: Use 'self.page' instead of 'page' inside class methods."
        return True, "OK"

    def _validate_hallucinations(self, code):
        """Checks for common autonomous hallucination patterns."""
        placeholders = ['locator_string', 'value', 'action_type', 'primary_locator', 'locator', 'action']
        for p in placeholders:
            # Look for variable usage without assignment OR as a param
            if re.search(fr"[ ,(]{p}[ ,)]", code) or re.search(fr"^{p}\b", code, re.MULTILINE):
                return False, f"Detected hallucinated placeholder variable: {p}"
        return True, "OK"

    def _validate_syntax(self, code):
        """Checks if code is valid Python using AST."""
        import ast
        try:
            ast.parse(code)
            return True, "OK"
        except SyntaxError as e:
            return False, f"SyntaxError at line {e.lineno}: {e.msg}\n{e.text}"
        except Exception as e:
            return False, f"Compilation Error: {e}"

    def review_and_fix(self, file_path, **kwargs):
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        print(f"🕵️  Reviewing {os.path.basename(file_path)}...")
        
        start_time = __import__('time').time()

        # 0. Pre-Check Syntax
        is_valid_syntax, syntax_error = self._validate_syntax(code_content)
        syntax_prompt_addendum = ""
        if not is_valid_syntax:
            print(f"⚠️ Initial Syntax Error Detected: {syntax_error}")
            syntax_prompt_addendum = f"\n\n**CRITICAL FIX REQUIRED**: The code currently has a SYNTAX ERROR. You MUST fix this:\n{syntax_error}"

        # Load Anti-Patterns for Quality Gate
        anti_path = os.path.join(os.path.dirname(__file__), "training/anti_patterns.json")
        anti_context = ""
        if os.path.exists(anti_path):
            try:
                with open(anti_path, "r", encoding="utf-8") as f:
                    anti = json.load(f)
                    anti_context = "\n**KNOWN ANTI-PATTERNS (REJECT THESE)**:\n"
                    for a in anti:
                        anti_context += f"- Mode: {a['failure_mode']}\n  Bad Pattern: `{a['bad_example']}`\n  Reason: {a['reason']}\n  Requirement: {a['fix']}\n"
            except: pass

        # Load Domain Rules
        domain = kwargs.get("domain", "general")
        domain_rules = ""
        domain_path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "domains", f"{domain}.yaml")
        if os.path.exists(domain_path):
            try:
                with open(domain_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    rules = data.get("learned_rules", [])
                    if rules:
                        domain_rules = "\n**LEARNED DOMAIN RULES (ENFORCE THESE)**:\n"
                        for r in rules:
                            domain_rules += f"- {r}\n"
            except: pass

        system_prompt = f'''You are a Principal Software Engineer in Test (SDET) with 15+ years of experience.
Your job is to CODE REVIEW and AUTO-FIX the provided Playwright Python script.

{anti_context}
{domain_rules}

**REVIEW CRITERIA (The "Bar"):**
1.  **Iterative Stability**: If the script iterates through dynamic lists (e.g., courses, products), REJECT standard `.all()` for loops. REQUIRE index-based loops (`nth(i)`) with re-navigation to prevent StaleElement errors.
2.  **Explicit Navigation Guards**: Every click that causes a URL change MUST be followed by `page.wait_for_url()` and `wait_for_stability()`.
3.  **Advanced Locator Priority**: Enforce the official Playwright priority hierarchy:
    - **1. User-Facing**: `get_by_role`, `get_by_label`, `get_by_placeholder`, `get_by_text`, `get_by_alt_text`, `get_by_title`.
    - **2. Test-Specific**: `get_by_test_id`.
    - **3. Fallback**: CSS selectors (shallow and simple only).
    - **4. Avoid**: XPath and deep/brittle CSS (e.g., `div > p > button`).
4.  **Chaining & Filtering**: Prefer chained filters over fragile CSS. REJECT positional selectors ( `.nth()`, `.first()`) if the element can be uniquely identified via context filtering (e.g., `.filter(has_text='Item 1')`).
5.  **Composite Logic**: Encourage the use of `.and_()` and hierarchical context (parent -> child) to create unique composite identifiers.
6.  **No Hardcoded Waits**: Remove `time.sleep()`. Use `expect(...).to_be_visible()` or `wait_for_load_state`.
7.  **Robust Locators**: Use `re.compile(..., re.IGNORECASE)` for text/role matches.
8.  **Assertions**: Code MUST have assertions (`expect(...)`). 
9.  **Standard API**: Prefer standard Playwright methods (`click()`, `fill()`) over custom helpers. Playwright has built-in auto-waiting.
10. **Syntax Integrity**: Ensure triple-quoted strings (<code>"""</code>) are properly closed.
11. **POM Scope**: Inside Page Object class methods, you MUST use `self.page` for all Playwright calls. NEVER use `page.` directly if not in the main test function.

**OUTPUT FORMAT**:
You must output a JSON object with this EXACT structure:
{{
  "status": "APPROVED" or "FIXED",
  "review_summary": "Brief bullet points of what you fixed or why it's good.",
  "final_code": "The complete, valid Python code (original or fixed)."
}}
'''
        
        user_msg = f"""
        Please review this Python Playwright test file:
        
        ```python
        {code_content}
        ```
        
        {syntax_prompt_addendum}
        """

        try:
            resp = self.llm.invoke([
                ("system", system_prompt),
                ("human", user_msg)
            ])
            
            result = self._try_parse_json(resp.content)
            
            if not result:
                print("⚠️ Reviewer returned invalid format. Skipping review.")
                return False, "Reviewer returned invalid JSON format."
            
            # Action
            if result.get("status") == "FIXED":
                print("⚠️ Code Issues Detected & Fixed:")
                print(result.get("review_summary", "No summary provided."))
                
                final_code = result.get("final_code")
                if final_code and len(final_code) > 50: # Sanity check
                    # Final Syntax Check
                    is_valid, reason = self._validate_syntax(final_code)
                    if not is_valid:
                        print(f"❌ Reviewer generated INVALID code: {reason}. Aborting write.")
                        return False, f"Reviewer generated INVALID code: {reason}"

                    # Write back the fixed code
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(final_code)
                    print("✅ Applied Fixes to File.")
                else:
                    print("⚠️ 'final_code' was empty or invalid. Skipping write.")
                    return False, "Reviewer 'final_code' was empty or invalid."
            else:
                # Post-LLM Analysis Syntax & Hallucination Check
                is_valid, reason = self._validate_syntax(result.get("final_code", code_content))
                if not is_valid:
                     print(f"❌ Reviewer REJECTED code due to syntax: {reason}")
                     return False, f"Reviewer REJECTED code due to syntax: {reason}"
                     
                is_valid, reason = self._validate_hallucinations(result.get("final_code", code_content))
                if not is_valid:
                    print(f"❌ Reviewer REJECTED code due to hallucinations: {reason}")
                    return False, f"Reviewer REJECTED code due to hallucinations: {reason}"
                
                is_valid, reason = self._validate_pom_scope(result.get("final_code", code_content))
                if not is_valid:
                    print(f"❌ Reviewer REJECTED code due to POM Scope: {reason}")
                    # If it's just a scope error, we could try to auto-fix it with LLM again or just reject
                    return False, f"Reviewer REJECTED code due to POM Scope: {reason}"
                    
                print("✅ Code Approved (No major issues found).")
            
            duration = __import__('time').time() - start_time
            logger.log_event("Reviewer", "review_code", duration, cost=0.01)
            
            return True, "Code Approved"

        except Exception as e:
            print(f"❌ Review Agent Crashed: {e}")
            return False, f"Review Agent Crashed: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reviewer.py <path_to_test_file>")
        sys.exit(1)
    
    path = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else "general"
    reviewer = CodeReviewer()
    success, msg = reviewer.review_and_fix(path, domain=domain)
    if not success:
        print(f"❌ Review Failed: {msg}")
        sys.exit(1)
