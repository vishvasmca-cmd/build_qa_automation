import os
import sys
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

class CodeReviewer:
    def __init__(self):
        load_dotenv()
        # Use JSON mode for structural reliability
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            temperature=0.1,
            model_kwargs={"response_mime_type": "application/json"}
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

    def review_and_fix(self, file_path):
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False

        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        print(f"🕵️  Reviewing {os.path.basename(file_path)}...")

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

        system_prompt = f'''You are a Principal Software Engineer in Test (SDET) with 15+ years of experience.
Your job is to CODE REVIEW and AUTO-FIX the provided Playwright Python script.

{anti_context}

**REVIEW CRITERIA (The "Bar"):**
1.  **Iterative Stability**: If the script iterates through dynamic lists (e.g., courses, products), REJECT standard `.all()` for loops. REQUIRE index-based loops (`nth(i)`) with re-navigation to prevent StaleElement errors.
2.  **Explicit Navigation Guards**: Every click that causes a URL change MUST be followed by `page.wait_for_url()` and `wait_for_stability()`.
3.  **Recursive "Start" Logic**: If the page has intermediate onboarding or roadmap screens, ensure the script has "Recursive Start" logic to handle 2-stage entry.
4.  **No Hardcoded Waits**: Remove `time.sleep()`. Use `expect(...).to_be_visible()` or `wait_for_load_state`.
5.  **Robust Locators**: Use `re.compile(..., re.IGNORECASE)` for text/role matches. Reject brittle XPaths.
6.  **Assertions**: Code MUST have assertions (`expect(...)`). 
7.  **Self-Healing**: Ensure critical actions use the `smart_action` helper (OR use Page Object methods if using POM).
8.  **Compilation Check**: REJECT any code that uses placeholder variables like `locator_string`, `value`, or `action_type` instead of actual values from the trace.
9.  **Protect Helpers**: DO NOT modify, delete, or "refactor" the boilerplate helper functions (`wait_for_stability`, `smart_action`) IF THEY EXIST. If using POM, these helpers might not be present - that is expected.
10. **Syntax Integrity**: Ensure that triple-quoted strings (`"""`) are ALWAYS properly closed with `"""`.

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
                return False
            
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
                        return False

                    # Write back the fixed code
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(final_code)
                    print("✅ Applied Fixes to File.")
                else:
                    print("⚠️ 'final_code' was empty or invalid. Skipping write.")
            else:
                # Post-LLM Analysis Syntax & Hallucination Check
                is_valid, reason = self._validate_syntax(result.get("final_code", code_content))
                if not is_valid:
                     print(f"❌ Reviewer REJECTED code due to syntax: {reason}")
                     return False
                     
                is_valid, reason = self._validate_hallucinations(result.get("final_code", code_content))
                if not is_valid:
                    print(f"❌ Reviewer REJECTED code due to hallucinations: {reason}")
                    return False
                    
                print("✅ Code Approved (No major issues found).")
            
            return True

        except Exception as e:
            print(f"❌ Review Agent Crashed: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reviewer.py <path_to_test_file>")
        sys.exit(1)
    
    path = sys.argv[1]
    reviewer = CodeReviewer()
    success = reviewer.review_and_fix(path)
    if not success:
        sys.exit(1)
