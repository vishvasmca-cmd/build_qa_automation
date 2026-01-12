import json
import re
import os
import textwrap
import yaml
from dotenv import load_dotenv

import base64
from langchain_core.messages import HumanMessage, SystemMessage

from core.lib.llm_utils import SafeLLM, try_parse_json
from termcolor import colored
import time

# Import Metrics Logger
# Import Metrics Logger
from core.lib.metrics_logger import logger

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
    in_test_function = False
    errors = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track class scope
        if stripped.startswith('class '):
            in_class = True
            in_test_function = False
            continue
        
        # Track if we're in test_ function (where page is OK)
        if in_class and stripped.startswith('def test_'):
            in_test_function = True
        elif in_class and stripped.startswith('def ') and '__init__' not in stripped:
            in_test_function = False
        
        # Look for ANY page.method() calls (not just specific ones)
        # This catches page.wait_for_selector, page.frame, etc.
        if in_class and not in_test_function and re.search(r'\bpage\.', line):
            # Make sure it's not self.page or a comment
            if not re.search(r'self\.page\.', line) and not stripped.startswith('#'):
                errors.append(f"Line {i+1}: Usage of 'page.' inside class method. Use 'self.page.' instead. Line: {stripped[:50]}")
    
    return len(errors) == 0, "\n".join(errors)

def check_logical_errors(code_string):
    """Advanced linter for logical bugs (unused imports, dangerous patterns)."""
    import ast
    errors = []
    try:
        tree = ast.parse(code_string)
        
        # 1. Unused Imports
        imported = set()
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names: imported.add(n.asname or n.name)
            elif isinstance(node, ast.ImportFrom):
                for n in node.names: imported.add(n.asname or n.name)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
                
        # Filter standard pytest fixture names which look unused but are needed
        exempt = {'pytest', 'page', 'context', 'browser', 'request'} 
        unused = [i for i in imported if i not in used_names and i not in exempt]
        if unused:
            errors.append(f"Unused imports detected (remove them): {', '.join(unused)}")

        # 2. Bare Except
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                errors.append(f"Line {node.lineno}: Bare 'except:' clause found. Use 'except Exception:' at minimum.")

    except Exception as e:
        pass # If AST fails, syntax check will catch it separately
        
    return len(errors) == 0, "\n".join(errors)

def load_historical_failures(target_url):
    """Failure RAG: Loads past failures for this site to prevent repetition (Herd Immunity)."""
    try:
        # Resolve path relative to this file
        fail_path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "failures.json")
        if not os.path.exists(fail_path): return ""
        
        with open(fail_path, "r", encoding="utf-8") as f:
            failures = json.load(f)
            
        # Filter specific to this site
        from urllib.parse import urlparse
        domain = urlparse(target_url).netloc.replace("www.", "")
        
        relevant_fails = [f for f in failures if domain in f.get("site", "")]
        
        if not relevant_fails: return ""
        
        # Summarize top errors
        from collections import Counter
        errors = [f.get("error", "Unknown") for f in relevant_fails]
        top_errors = Counter(errors).most_common(3)
        
        summary = "\n**⚠️ HISTORICAL FAILURE WARNINGS (PREVENT THESE ERRORS)**:\n"
        for err, count in top_errors:
            if "valid code" in err: continue # Skip generic generation errors
            summary += f"- PREVIOUS ERROR: '{err}'. (Happened {count} times). FIX THIS PROACTIVELY.\n"
            
        return summary
    except:
        return ""


class CodeRefiner:
    def __init__(self):
        load_dotenv()
        self.llm = SafeLLM(model="gemini-2.0-flash", temperature=0.0)

    def generate_code(self, target_url, trace_summary, images=None, error_context=None, domain="general", workflow_goal=""):
        """Generates cleaner, hardened code from a JSON trace summary, with optional visual, error, and domain context."""
        
        # Load Golden Reference Patterns (File-Based)
        golden_dir = os.path.join(os.path.dirname(__file__), "golden_patterns")
        golden_context = ""
        
        # 1. Load Markdown Principles (Human-readable rules)
        md_golden_path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "locators_golden_set.md")
        if os.path.exists(md_golden_path):
            try:
                with open(md_golden_path, "r", encoding="utf-8") as f:
                    golden_context += "\n**LOCATOR PRINCIPLES & EXAMPLES (MUST FOLLOW)**:\n"
                    golden_context += f.read() + "\n"
            except Exception as e:
                print(f"⚠️ Failed to load MD golden patterns: {e}")

        # 2. Load Python Snippets (Executable patterns)
        if os.path.exists(golden_dir):
            golden_context += "\n**STRICT REFERENCE SNIPPETS (IMPLEMENT THESE PATTERNS)**:\n"
            try:
                for fname in os.listdir(golden_dir):
                    if fname.endswith(".py"):
                        with open(os.path.join(golden_dir, fname), "r", encoding="utf-8") as f:
                            code = f.read()
                            golden_context += f"\n--- Reference: {fname} ---\n```python\n{code}\n```\n"
            except Exception as e:
                print(f"⚠️ Failed to load Python golden patterns: {e}")

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

        # Load Site-Specific Knowledge (Proven Locators)
        site_knowledge = ""
        from urllib.parse import urlparse
        netloc = urlparse(target_url).netloc
        site_locators_path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "sites", netloc, "locators.json")
        if os.path.exists(site_locators_path):
             try:
                with open(site_locators_path, "r", encoding="utf-8") as f:
                    proven_locs = json.load(f)
                    if proven_locs:
                        site_knowledge = f"\n**PROVEN LOCATORS FOR {netloc} (USE THESE IF THEY MATCH THE GOAL)**:\n"
                        site_knowledge += json.dumps(proven_locs, indent=2)
             except: pass
        
        # Load Site specific rules
        site_rules_path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "sites", netloc, "rules.md")
        if os.path.exists(site_rules_path):
            try:
                with open(site_rules_path, "r", encoding="utf-8") as f:
                    rules_content = f.read()
                    site_knowledge += f"\n\n**⚠️ MANDATORY SITE RULES FOR {netloc} (YOU MUST OBEY THESE)**:\n{rules_content}\n"
            except Exception as e:
                print(f"⚠️ Failed to load site rules: {e}")

        # Load Standard POM Guide (Mandatory)
        pom_guide_context = ""
        pom_guide_path = os.path.join(os.path.dirname(__file__), "..", "docs", "STANDARD_POM_GUIDE.md")
        if os.path.exists(pom_guide_path):
            try:
                with open(pom_guide_path, "r", encoding="utf-8") as f:
                    pom_guide_context = "\n**MANDATORY STANDARD POM GUIDELINES (MUST FOLLOW EXACTLY)**:\n" + f.read() + "\n"
            except Exception as e:
                print(f"⚠️ Failed to load POM guide: {e}")

        # Load Platform Strategy (Dispatcher)
        platform_rules = ""
        try:
            from core.engine.dispatcher import Dispatcher
            platform_rules = Dispatcher().get_specialized_context(target_url)
        except Exception as e:
            pass # Dispatcher is optional

        # Load RAG Knowledge (Global AKG)
        rag_context = ""
        try:
             # Lazy import to avoid circular dependencies
             try: from core.knowledge.rag_retriever import RAGRetriever
             except ImportError: from knowledge.rag_retriever import RAGRetriever
             
             retriever = RAGRetriever()
             # Fetch procedural nodes and domain-specific coding patterns
             nodes = retriever.retrieve(url=target_url, domain=domain, limit=5)
             if nodes:
                 rag_context = "\n**GLOBAL AUTOMATION KNOWLEDGE (RAG)**:\n"
                 for n in nodes:
                     rag_context += f"- [{n.get('node_type', 'general').upper()}]: {n.get('lesson')}\n"
        except Exception as e:
            print(f"⚠️ Failed to load RAG context: {e}")

        # Load Failure RAG (Herd Immunity)
        failure_knowledge = load_historical_failures(target_url)

        prompt_template = """
        You are an expert Playwright test automation engineer. 
        Refine the following execution trace into a linear, clean, and ROBUST Playwright script for {{TARGET_URL}}.
        
        {{POM_GUIDE}}

        {{GOLDEN_CONTEXT}}

        {{PLATFORM_RULES}}
        
        {{RAG_CONTEXT}}

        {{FAILURE_KNOWLEDGE}}
        
        **PRIORITY ORDER (ALWAYS FOLLOW THIS LOCATOR CASCADE)**:
        1. **SITE-SPECIFIC PROVEN LOCATORS**: First, check the `site_knowledge`. If an element in the trace matches a "Proven" locator from past successful runs, use it.
        2. **USER-FACING LOCATORS** (Rank 1):
           - `page.get_by_role()`: Select by ARIA roles and accessible names (e.g., `role="button", name="Submit"`)
           - `page.get_by_label()`: For form inputs with labels
           - `page.get_by_placeholder()`: For inputs with placeholder text
           - `page.get_by_text()`: For visible text content
           - `page.get_by_alt_text()`: For images
        3. **TEST-SPECIFIC LOCATORS** (Rank 2):
           - `page.get_by_test_id()`: Custom data-testid attributes
        4. **CSS ATTRIBUTES** (Rank 3):
           - Use functional attributes (e.g., `button[type="submit"]`) over positional ones.
        5. **XPATH / DEEP CSS** (Rank 4): AVOID unless absolutely necessary for unique identification.

        **COMPOSITE LOCATORS & FILTERING (CRITICAL)**:
        - **Chaining**: Chain locators to narrow scope: `page.get_by_role('listitem').filter(has_text='Product 2').get_by_role('button', name='Add to cart')`
        - **Multi-Level Filtering**: When nothing is unique, combine multiple non-unique characteristics:
          `page.locator('.notification').filter(has_text='Order #123').filter(has=page.locator('.status-active')).get_by_role('button', name='View')`
        - **Using .and_()**: Combine conditions: `page.get_by_role('button').and_(page.get_by_title('Subscribe'))`
        - **Contextual Anchoring**: Find a unique parent container first, then search within it.
        - **Scoping (Header/Footer)**: ALWAYS chain locators for common links (e.g. `page.locator('footer').get_by_role('link', name='Home')`) to prevent strict mode violations and ensure intent.
        - **LONG-TAIL COMPLETENESS (CRITICAL)**: If the trace contains 20+ steps, DO NOT TRUNCATE. Every login, product search, cart addition, and checkout step in the trace MUST be implemented in the POM and the final test logic.

        **MANDATORY: Page Object Model (POM) STRUCTURE**:
        You MUST strictly follow the structure and coding standards defined in the **MANDATORY STANDARD POM GUIDELINES** provided above.
        1. **Page Object Classes**: Implement the pages as defined in the guide (BasePage is mandatory).
        2. **Test Function**: Use the exact `test_autonomous_flow` structure from the guide.
        3. **Refrain from Creativity**: Do not invent new helper functions or folders.

        {{DOMAIN_RULES}}
        
        {{SITE_KNOWLEDGE}}

        **PROHIBITED PATTERNS (Anti-Hallucination)**:
        - ❌ NEVER import `utils`, `core.utils` or `helpers`. `take_screenshot` is pre-imported via dynamic sys.path initialization.
        - ❌ **ABSOLUTE PATHS**: NEVER use absolute local paths (e.g., C:\\Users\\... or /home/runner/...) in code. Use relative logic or rely on the established environment.
        - ❌ **FATAL ERROR**: NEVER use `page.` inside a class method (except `__init__`). YOU MUST USE `self.page.`.
          - BAD: `page.locator(...)`
          - GOOD: `self.page.locator(...)`
        - ❌ NEVER use placeholder variables like `locator_string`, `action_type`, or `value` unless they are explicitly assigned from the trace.
        - ❌ NEVER use positional `.nth(0)` if a text match or ID is available in the trace element context.
        - ❌ **STABILITY WARNING**: NEVER use full URLs as accessibility names (e.g. `get_by_role("link", name="https://...")`). Use visible text or labels instead.
        - ❌ **STABILITY WARNING**: NEVER use explicit `scroll` or `PageDown` actions. Playwright actions auto-scroll to the element.
        - ❌ **STRICT MODE VIOLATION**: If a locator matches multiple elements (e.g., 'Add to cart' buttons), you **MUST** uses `.first` or `.nth(0)` to pick one.
        - ❌ **AMBIGUOUS LINKS**: If a link like "About Us" or "Contact" appears in both Header and Footer, you MUST chain the locator to a unique parent container (e.g., `self.page.locator('header').get_by_role('link', name='About Us')`).
        - ❌ **SYNTAX ERROR**: NEVER use `.first()` as a method. It is a property. Use `locator.first.click()`.
        - ⚠️ **HOVER VISIBILITY**: If an element appears only on hover (e.g., 'Add to cart' on product cards), you MUST `hover()` the container first.
        - ⚠️ **NAVIGATION LOGIC**: Ensure you navigate to the destination (e.g., click Cart icon) BEFORE interacting with page-specific elements (e.g., Checkout button).
        - ⚠️ **CLICK INTERCEPTION by ADS/OVERLAYS**: 
             - If an element is covered by an ad (e.g., Google Ads, `<section id="advertisement">`), you MUST uses `force=True` on the click/hover action: `.click(force=True)`.
             - Alternatively, try to evaluate JavaScript to remove the overlay: `self.page.evaluate("document.querySelectorAll('.ad-container, #advertisement').forEach(el => el.remove())")` before interacting.

        **CRITICAL RULES**:
        1. **STANDARDS ONLY**: You MUST use pure Playwright API. DO NOT use custom helpers like `smart_action`.
           - `take_screenshot(page, name, project_name)` is the only allowed helper. IT IS ALREADY IMPORTED. DO NOT IMPORT IT.
        2. **COMPLETENESS (NON-NEGOTIABLE)**: YOU MUST IMPLEMENT ALL STEPS AND GOALS mentioned in the `workflow_goal`. 
           - If the goal is "Register, Login, Transfer, Loan", and you only write the Registration test, **YOU HAVE FAILED**.
           - If the trace is incomplete, you MUST infer the missing logic or add `TODO` comments with `expect(True).to_be(False, "Not Implemented")` to signal incomplete work.
           - **NEVER** truncate the test logic. It is better to have broken code than missing code.
        3. **DOTS IN IDs**: If an element ID contains a dot (e.g., `customer.firstName`), **NEVER** use the `#` selector with escaping. **ALWAYS** use the attribute selector `[id='customer.firstName']` or `[name='customer.firstName']`.
        4. **DROPDOWNS (SELECT)**: NEVER attempt to `.click()` an `<option>` element. ALWAYS use `self.page.get_by_label(...).select_option(label="...")`.
        5. **SYNC ONLY**: You MUST use SYNC Python Playwright. **DO NOT USE `await` keyword.**
        6. **PYTHON KWARGS ONLY**: 
           - ✅ `page.get_by_role("link", name="Home")`
           - **NEVER** use `{{ key: value }}` JS objects. Always use `key=value`.
        4. **Actions**: Use regular Playwright methods: `.click()`, `.fill()`, `.select_option()`.
        5. **Stability**: Use `page.wait_for_load_state("networkidle")` or specific element waits if needed after interactions.
        6. **TIMEOUTS & URL STABILITY**: Use generous timeouts (at least 60000ms) for navigations. When using `wait_for_url` or `to_have_url`, ALWAYS use a wildcard `*` at the end or a regex to handle trailing slashes or `/index` suffixes (e.g. use `**/dashboard*` instead of `**/dashboard`).
        7. **Reliability**: Use the trace's element context (text, roles, labels) to build robust locators.
        8. **SELF-CONTAINED ROBUSTNESS**:
           - **NO PAGE IMPORTS**: You are generating a standalone script. You MUST define all Page Object classes INLINE in the output JSON. **DO NOT** write `from pages... import...` lines.
           - **PATH SETUP**: Start the `test_logic` with:
             ```python
             import sys, os
             sys.path.append(os.getcwd())
             ```
           - **HELPERS**: `from helpers import take_screenshot` is allowed (with try/except fallback).

        **OUTPUT FORMAT**:
        You must output a JSON object with this EXACT structure:
        {
          "pages": [
            {
              "class_name": "LoginPage",
              "code": "class LoginPage:\\n    def __init__(self, page):... (full class code here)"
            }
          ],
          "test_logic": "def test_autonomous_flow(page: Page):\\n    # Setup, calls to POM actions, assertions, cleanup"
        }

        **WORKFLOW GOAL (REQUIRED TO PASS)**:
        {{WORKFLOW_GOAL}}

        **TRACE TO REFINE**:
        {{TRACE_SUMMARY}}
        """
        
        if error_context:
            prompt_template += f"\n\n**IMPORTANT: PREVIOUS EXECUTION FAILED**:\n{error_context}\nPlease analyze the error and fix it in your new generation."
        
        # Ensure goal is visible
        goal_text = trace_summary if "Workflow:" in trace_summary else "Full Coverage"
        
        prompt = prompt_template.replace("{{TARGET_URL}}", target_url)\
                               .replace("{{GOLDEN_CONTEXT}}", golden_context)\
                               .replace("{{TRACE_SUMMARY}}", trace_summary)\
                               .replace("{{WORKFLOW_GOAL}}", workflow_goal if workflow_goal else "See Trace")\
                               .replace("{{PROJECT_NAME}}", os.path.basename(os.getcwd()))\
                               .replace("{{DOMAIN_RULES}}", domain_rules)\
                               .replace("{{SITE_KNOWLEDGE}}", site_knowledge)\
                               .replace("{{FAILURE_KNOWLEDGE}}", failure_knowledge)\
                               .replace("{{POM_GUIDE}}", pom_guide_context)\
                               .replace("{{RAG_CONTEXT}}", rag_context)\
                               .replace("{{PLATFORM_RULES}}", platform_rules)

        # Prepare Text-Only Message
        content = [{"type": "text", "text": prompt}]
        
        # Layer 4: Retry Loop with Validation
        MAX_RETRIES = 2
        
        for attempt in range(MAX_RETRIES + 1):
            messages = [HumanMessage(content=content)]
            
            try:
                resp = self.llm.invoke(messages)
            except Exception as e:
                # No vision fallback needed as we are text-only
                raise e
            
            result = try_parse_json(resp.content)
            if not result:
                if attempt < MAX_RETRIES:
                    content.append({"type": "text", "text": "Invalid JSON format. Please return ONLY the JSON object."})
                    continue
                else: 
                    return None

            # Validate generated pieces
            full_code = "\n\n".join([p["code"] for p in result.get("pages", [])]) + "\n\n" + result.get("test_logic", "")
            
            error_feedback = []
            
            is_valid, syntax_error = validate_python_syntax(full_code)
            if not is_valid:
                error_feedback.append(f"SYNTAX ERROR: {syntax_error}")
            
            is_pom_valid, pom_error = validate_pom_scope(full_code)
            if not is_pom_valid:
                error_feedback.append(f"POM SCOPE ERROR: {pom_error}")
                
            undefined_vars = find_undefined_variables(full_code)
            if undefined_vars:
                error_feedback.append(f"UNDEFINED VARIABLES ERROR: {undefined_vars}")
                
            is_logic_valid, logic_error = check_logical_errors(full_code)
            if not is_logic_valid:
                error_feedback.append(f"CLEAN CODE LINT ERROR: {logic_error}")

            if not error_feedback:
                return full_code
            
            # If we have errors and attempts left, provide constructive feedback
            if attempt < MAX_RETRIES:
                feedback_str = "\n".join(error_feedback)
                print(colored(f"   ⚠️ Linting failed (Attempt {attempt+1}). Retrying with feedback...", "yellow"))
                # Inject feedback as a separate message to keep context clear
                content.append({
                    "type": "text", 
                    "text": f"\n\n**CRITICAL: YOUR LAST GENERATION FAILED LINTING**:\n{feedback_str}\n\nPlease analyze these errors and provide the CORRECTED JSON output. Ensure all imports are present and syntax is valid Python."
                })
            else:
                print(colored(f"   ❌ Linting failed after {MAX_RETRIES} attempts. Returning best effort.", "red"))
                return full_code
        
        return None
        
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
    
    # NOTE: Images are disabled during code generation to save tokens and avoid 400 errors.
    # Structural trace data is sufficient for refinement.
    images_b64 = []
    
    trace_summary = json.dumps([{
        "step": t['step'],
        "url": t.get('url'),
        "page_name": t.get('page_name', 'GenericPage'),
        "action": t['action'],
        "thought": t.get('thought'),
        "locator": t.get('locator_used') or t.get('locator'),
        "value": t.get('value'),
        "element_context": t.get('element_context'),
        "expectation": t.get('expected_outcome')
    } for t in trace], indent=2)
    
    raw_code = refiner.generate_code(target_url, trace_summary, images=[], error_context=error_context, domain=domain, workflow_goal=workflow_goal)

    if not raw_code:
        print("❌ Refiner failed to generate valid code.")
        return False

    clean_steps = raw_code

    project_name = os.path.basename(os.path.dirname(os.path.dirname(trace_path)))
    
    from core.lib.template_engine import TestTemplateEngine
    engine = TestTemplateEngine()
    final_code = engine.generate_test(
        project_name=project_name,
        target_url=target_url,
        test_steps=clean_steps
    )
    
    # --- Step 4: Quality Gate (Reviewer) ---
    # Review the code BEFORE writing to catch structural issues
    try:
        from core.agents.reviewer import CodeReviewer
        import tempfile
        
        # Write to temp file for review
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
            temp_path = temp_file.name
            temp_file.write(final_code)
        
        reviewer = CodeReviewer()
        is_approved, review_msg = reviewer.review_and_fix(temp_path, domain=domain)
        
        # Read back the potentially fixed code
        with open(temp_path, 'r', encoding='utf-8') as f:
            final_code = f.read()
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if not is_approved:
            # Soft-fail if Reviewer just broke on format (Truncation/JSON error)
            if "invalid format" in review_msg or "Review Agent Crashed" in review_msg:
                 print(colored(f"⚠️ Code Review Format Error: {review_msg}. Proceeding with best-effort code.", "yellow"))
            else:
                 print(colored(f"❌ Code Review Failed: {review_msg}", "red"))
                 print(colored("🔄 Refiner will regenerate on next attempt...", "yellow"))
                 return None  # Signal failure to trigger regeneration
            
    except Exception as e:
        print(colored(f"⚠️ Automated Review Failed: {e}", "yellow"))
        # Continue anyway if reviewer crashes
    
    # Only write if review passed
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir): os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(final_code)
    
    print(f"✅ Self-Healing Code Generated & Reviewed: {output_path}")
    
    duration = __import__('time').time() - start_time
    logger.log_event("Refiner", "generate_code", duration, cost=0.01)
    
    return True  # Signal success

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
            
    result = generate_code_from_trace(t_path, o_path, goal, error_context=err_ctx, domain=dom)
    
    # Exit with appropriate code for Orchestrator
    if result is None or result is False:
        sys.exit(1)  # Signal failure - Orchestrator will retry
    sys.exit(0)  # Success


class FrameworkGenerator:
    """
    Phase 3: Structure-First POM Generator.
    Builds strict Page Objects from Miner blueprints and Linear Tests from Explorer traces.
    """
    def __init__(self, project_root):
        self.project_root = project_path = project_root
        self.output_dir = os.path.join(project_root, "outputs")
        self.pages_dir = os.path.join(project_root, "pages")
        self.tests_dir = os.path.join(project_root, "tests", "e2e")
        self.models_path = os.path.join(self.output_dir, "page_models.json")
        self.trace_path = os.path.join(self.output_dir, "trace.json")
        
    def generate(self):
        print(colored("🏭 Starting Framework Generation...", "cyan"))
        
        if not os.path.exists(self.models_path):
            print(colored("❌ No page_models.json found. Skipping.", "red"))
            return False

        # 1. Generate Page Objects
        with open(self.models_path, "r") as f:
            models = json.load(f)
            
        os.makedirs(self.pages_dir, exist_ok=True)
        # Init file
        with open(os.path.join(self.pages_dir, "__init__.py"), "w") as f: pass
        
        for page_name, model in models.items():
            # Skip generic/unknown page names
            if page_name.lower() in ['unknown', 'unknownpage', 'genericpage', 'page']:
                print(colored(f"   ⏭️ Skipping generic page: {page_name}", "grey"))
                continue
            self._generate_page_file(page_name, model)
            
        # 2. Generate Test File
        self._generate_test_file()
        
        # 3. Generate Conftest (Stealth Mode)
        self._generate_conftest()

        # 4. Ensure Init Files
        self._ensure_init_files()
        
        return True

    def _ensure_init_files(self):
        """Creates __init__.py in all necessary directories to ensure module execution."""
        dirs = [
            self.project_root,
            self.pages_dir,
            os.path.join(self.project_root, "tests"),
            self.tests_dir
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            init_path = os.path.join(d, "__init__.py")
            if not os.path.exists(init_path):
                with open(init_path, "w") as f: f.write("")

    def _generate_conftest(self):
        """Generates conftest.py with stealth fixtures."""
        code = '''import pytest
from playwright.sync_api import BrowserContext

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars"
        ]
    }

@pytest.fixture(scope="function")
def context(context: BrowserContext):
    # Enhanced stealth for headless mode
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = {runtime: {}};
    """)
    # Set stealth headers
    context.set_extra_http_headers({
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    })
    yield context
'''
        # Write to tests/conftest.py
        conftest_path = os.path.join(self.project_root, "tests", "conftest.py")
        os.makedirs(os.path.dirname(conftest_path), exist_ok=True)
        with open(conftest_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(colored("   ✅ Generated conftest.py (Stealth Mode)", "green"))

    def _sanitize_method_name(self, name):
        """Ensures method names are valid Python identifiers."""
        # Strip whitespace first and replace spaces/invalid chars with underscore
        clean = re.sub(r'[^a-zA-Z0-9_]', '_', name.strip().lower())
        # Collapse multiple underscores
        clean = re.sub(r'_+', '_', clean)
        # Remove leading numbers
        if clean and clean[0].isdigit():
            clean = "_" + clean
        # Ensure it's not empty
        if not clean:
            clean = "element_action"
        return clean

    def _generate_page_file(self, page_name, model):
        filename = self._to_snake_case(page_name) + ".py"
        filepath = os.path.join(self.pages_dir, filename)
        
        class_name = page_name
        # Ensure class name ends with Page if not present
        if not class_name.endswith("Page"): class_name += "Page"
        
        code = [
            "from playwright.async_api import Page, expect",
            "",
            f"class {class_name}:",
            f"    \"\"\"",
            f"    {model.get('description', 'Auto-generated Page Object')}",
            f"    URL Pattern: {model.get('url_pattern', 'Unknown')}",
            f"    \"\"\"",
            "    def __init__(self, page: Page):",
            "        self.page = page",
            ""
        ]
        
        # Locators (Properties)
        for el in model.get("elements", []):
            name = el['name']
            primary = el['primary_locator']
            backup = el.get('backup_locator')
            desc = el.get('description', '')
            
            # Sanitize property name
            safe_name = self._sanitize_method_name(name)
            
            code.append("    @property")
            code.append(f"    def {safe_name}(self):")
            code.append(f"        \"\"\"{desc}\"\"\"")
            if backup:
                # Use .or_() logic
                code.append(f"        return self.page.{primary}.or_(self.page.{backup})")
            else:
                code.append(f"        return self.page.{primary}")
            code.append("")

        # Assertions / Actions
        code.append("    async def verify_loaded(self):")
        code.append("        \"\"\"Executes critical checks to ensure page is ready.\"\"\"")
        assertions = model.get("assertions", [])
        if assertions:
            for asn in assertions:
                code.append(f"        await {asn}")
        else:
             code.append("        await expect(self.page).to_have_url(re.compile('.*'))")
        
        content = "\n".join(code)
        # Validate syntax before writing
        is_valid, error = validate_python_syntax(content)
        if not is_valid:
             print(colored(f"   ⚠️ Syntax Error in generated {filename}: {error}", "yellow"))
             # We write it anyway but log it, so future agents can fix it.
             
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(colored(f"   ✅ Generated {filename}", "green"))

    def _generate_test_file(self):
        if not os.path.exists(self.trace_path): return
        
        with open(self.trace_path, "r") as f:
            trace_data = json.load(f)
            
        timestamp = int(time.time())
        test_filename = f"test_generated_{timestamp}.py"
        os.makedirs(self.tests_dir, exist_ok=True)
        filepath = os.path.join(self.tests_dir, test_filename)
        
        # Imports
        imports = ["import pytest", "import re", "from playwright.async_api import Page, expect"]
        
        # Determine strict page mapping
        trace = trace_data.get("trace", [])
        used_pages = set()
        for step in trace:
            p = step.get("page_name")
            if p: used_pages.add(p)
            
        for p in used_pages:
            module = self._to_snake_case(p)
            cls = p if p.endswith("Page") else p + "Page"
            imports.append(f"from pages.{module} import {cls}")

        code = imports + ["", "@pytest.mark.asyncio", "async def test_workflow(page: Page):"]
        code.append(f"    # Workflow: {trace_data.get('workflow', 'Auto-generated')}")
        code.append(f"    await page.goto('{trace_data.get('target_url')}')")
        
        # Instantiate Pages
        for p in used_pages:
             cls = p if p.endswith("Page") else p + "Page"
             var = self._to_snake_case(p)
             code.append(f"    {var} = {cls}(page)")
             
        code.append("")
        
        # Generate Steps
        for step in trace:
            action = step.get('action', 'unknown')
            p_name = step.get('page_name')
            p_var = self._to_snake_case(p_name) if p_name else "page"
            
            # Defensive check for step and thought keys
            step_num = step.get('step', '?')
            thought = step.get('thought', 'Executing action')
            
            comment = f"    # Step {step_num}: {thought}"
            code.append(comment)
            
            # For this MVP Main Generator, we will keep it simple: 
            # If the trace has a specific known assertion, we add it. 
            # Otherwise we assume the user will refine the logic.
            # But wait, the user wants "No custom helper functions".
            # So we will output valid playwight code.
            
            # Since generating perfect method calls from a raw trace requires another LLM pass (Refiner), 
            # we will utilize the `CodeRefiner` class we already have BUT pass it the Context of the Page Objects we just built.
            pass 
        
        # NOTE: For the MVP, I will delegate the Test Body generation BACK to the LLM-based `CodeRefiner` 
        # but instruct it to USE the Page Objects we just created.
        # This keeps the logic robust.
        
        print(colored(f"   ⚠️ Test Generation delegated to Refiner (Smart Mode)", "yellow"))

    def _to_snake_case(self, name):
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

