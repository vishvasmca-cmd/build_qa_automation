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

    def generate_code(self, target_url, trace_summary, pom_context="", images=None, error_context=None, domain="general", workflow_goal=""):
        """Generates clean TypeScript Playwright code mapping trace to POMs."""
        
        prompt_template = """
        You are an expert Node.js Playwright automation engineer.
        Your goal is to write a TypeScript test file (`workflow.spec.ts`) that implements the following workflow.
        
        **MANDATORY ARCHITECTURE**:
        1. **Page Objects**: Use the already generated Page Objects in the `../../pages/` directory.
        2. **Resilience**: Use the POM's getters (locators). Always prefer them over raw Playwright locators.
        3. **Interaction Stability**: For navigational menus or buttons likely to be intercepted, use `.click({ force: true })` or `.hover()` followed by a click.
        4. **Agent Planning**: For high-level steps or recovering from complex page states, use `await pageObject.agentExecute('Strategic Goal Description')`.
        5. **Stability**: Use `await page.goto(...)` or the POM's `goto` method. Prefer `domcontentloaded` if explicit waiting is needed.
        
        **POM CONTEXT (AVAILABLE METHODS)**:
        {{POM_CONTEXT}}
        
        **DOM CONTEXT**:
        {{TRACE_SUMMARY}}
        
        **WORKFLOW GOAL**:
        {{WORKFLOW_GOAL}}
        
        **OUTPUT FORMAT**:
        Return a JSON object with this exact structure:
        {
          "imports": "import { test, expect } from '@playwright/test';\\nimport { HomePage } from '../../pages/HomePage';\\n...",
          "test_logic": "test('Autonomous Workflow', async ({ page }) => {\\n    const homePage = new HomePage(page);\\n    await homePage.goto('{{TARGET_URL}}');\\n    ..."
        }
        """
        
        prompt = prompt_template.replace("{{TARGET_URL}}", target_url)\
                               .replace("{{POM_CONTEXT}}", pom_context)\
                               .replace("{{TRACE_SUMMARY}}", trace_summary)\
                               .replace("{{WORKFLOW_GOAL}}", workflow_goal if workflow_goal else "Complete the audit")
                               
        if error_context:
            prompt += f"\n\n**FIX PREVIOUS ERROR**: {error_context}"

        messages = [HumanMessage(content=[{"type": "text", "text": prompt}])]
        
        try:
            resp = self.llm.invoke(messages)
            result = try_parse_json(resp.content)
            if not result: return None
            
            full_code = result.get("imports", "") + "\n\n" + result.get("test_logic", "")
            return full_code
        except Exception as e:
            print(f"❌ Refiner LLM Error: {e}")
            return None
        
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
        
        # 1a. Generate BasePage (Infrastructure)
        self._generate_base_page()
        
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

        # 4. Generate Project Configs (Node.js)
        self._generate_package_json()
        self._generate_playwright_config()

        # 5. Ensure Init Files
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
    def _generate_package_json(self):
        """Generates package.json for the Node.js Playwright project."""
        project_name = os.path.basename(self.project_root)
        content = {
            "name": project_name,
            "version": "1.0.0",
            "description": "Auto-generated Playwright E2E tests",
            "scripts": {
                "test": "playwright test"
            },
            "devDependencies": {
                "@playwright/test": "^1.40.0"
            }
        }
        filepath = os.path.join(self.project_root, "package.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)
        print(colored("   ✅ Generated package.json", "green"))

    def _generate_playwright_config(self):
        """Generates playwright.config.ts for reliable test discovery."""
        code = '''import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    trace: 'on-first-retry',
    viewport: { width: 1280, height: 800 },
    ignoreHTTPSErrors: true,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    }
  ],
});
'''
        filepath = os.path.join(self.project_root, "playwright.config.ts")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(colored("   ✅ Generated playwright.config.ts", "green"))

    def _generate_base_page(self):
        """Generates BasePage.ts with Smart Locator and Agentic capabilities."""
        code = '''import { Page, Locator, expect } from '@playwright/test';

export interface SmartLocatorConfig {
    role?: [string, any];
    text?: string;
    testId?: string;
    label?: string;
    placeholder?: string;
    css?: string;
    xpath?: string;
    iframe?: string;
}

/**
 * BasePage provides the Foundation for all Page Objects, 
 * including Resilient Locators and Agentic Execution.
 */
export class BasePage {
    readonly page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    async goto(url: string) {
        await this.page.goto(url);
        await this.dismissPopups();
        await this.page.waitForTimeout(2000); // Let layout settle after popups
    }

    /**
     * Resilient Smart Locator: Chained strategies with .or()
     */
    protected smartLocator(config: SmartLocatorConfig): Locator {
        let root = this.page as any;
        if (config.iframe) {
            root = this.page.frameLocator(config.iframe);
        }

        let locator: Locator | undefined;

        if (config.testId) {
            locator = root.getByTestId(config.testId).filter({ visible: true }).first();
        }

        if (config.role) {
            const [roleName, options] = config.role;
            const l = root.getByRole(roleName as any, options).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }

        if (config.label) {
            const l = root.getByLabel(config.label).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }

        if (config.text) {
             // Use RegExp for flexible text matching (handles spacers, icons, etc)
             const l = root.getByText(new RegExp(config.text, "i")).filter({ visible: true }).first();
             locator = locator ? locator.or(l) : l;
        }

        if (config.css) {
            const l = root.locator(config.css).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }
        if (config.xpath) {
            const l = root.locator(config.xpath).filter({ visible: true }).first();
            locator = locator ? locator.or(l) : l;
        }

        if (!locator) {
            throw new Error("SmartLocator must have at least one strategy defined.");
        }

        return locator;
    }

    /**
     * Agent Mode: Execute a high-level task using AI Planning.
     * Transitions from "Command Execution" (how) to "Strategic Goal" (what).
     */
    async agentExecute(goal: string) {
        console.log(`\n\n[🤖 AGENT] Planning strategically for goal: "${goal}"`);
        
        // 1. Snapshot the state for the Planner
        const state = {
            url: this.page.url(),
            title: await this.page.title(),
            viewport: this.page.viewportSize(),
        };
        
        console.log(`[🤖 AGENT] Current URL: ${state.url}`);
        
        // 2. Resilience Loop: Handle unpredictable obstacles
        await this.dismissPopups();
        
        // 3. Strategic Execution (Placeholder for live LLM bridge)
        // In a full integration, this would call a local agent API to get the next step.
        // For now, it provides the hook for the Orchestrator to monitor and assist.
        console.log(`[🤖 AGENT] Strategy mapped. Executing interaction...`);
        
        await this.page.waitForLoadState('networkidle');
    }

    /**
     * Internal: Handle generic page obstacles (Overlays, Modals, Cookie Banners)
     */
    protected async dismissPopups() {
        const triggers = [
            'button:has-text("Accept")', 
            'button:has-text("Reject")',
            'button:has-text("Got it")',
            'button:has-text("Agree")',
            '#onetrust-accept-btn-handler',
            '.cookie-accept',
            '[aria-label="Close"]', 
            '.close-button', 
            '#dismiss'
        ];
        for (const selector of triggers) {
            try {
                const el = this.page.locator(selector).first();
                if (await el.isVisible({ timeout: 2000 })) {
                    console.log(`[🤖 AGENT] Clearing obstacle: ${selector}`);
                    await el.click({ force: true });
                }
            } catch (e) {}
        }
    }
}
'''
        filepath = os.path.join(self.pages_dir, "BasePage.ts")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(colored("   ✅ Generated BasePage.ts (Enhanced Agentic Interface)", "green"))

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





    def _sanitize_method_name(self, name):
        """Ensures method names are valid identifiers."""
        clean = re.sub(r'[^a-zA-Z0-9_]', '_', name.strip().lower())
        clean = re.sub(r'_+', '_', clean)
        if clean and clean[0].isdigit():
            clean = "_" + clean
        return clean or "element_action"

    def _generate_page_file(self, page_name, model):
        filename = page_name + ".ts"
        filepath = os.path.join(self.pages_dir, filename)
        
        class_name = page_name
        if not class_name.endswith("Page"): class_name += "Page"

        code = [
            "import { Page, Locator, expect } from '@playwright/test';",
            "import { BasePage } from './BasePage';",
            "",
            f"export class {class_name} extends BasePage {{",
            "    /**",
            f"     * {model.get('description', 'Auto-generated Page Object')}",
            f"     * URL Pattern: {model.get('url_pattern', 'Unknown')}",
            "     */",
            ""
        ]
        
        for el in model.get("elements", []):
            name = el['name']
            primary = el['primary_locator']
            backup = el.get('backup_locator')
            desc = el.get('description', '')
            
            safe_name = self._sanitize_method_name(name)
            
            # Construct SmartConfig
            strategies = []
            if primary: strategies.append(self._guess_strategy(primary))
            if backup: strategies.append(self._guess_strategy(backup))
            
            # Formatting JSON for TypeScript
            config_str = "{\n"
            for key, val in strategies:
                if key == 'role':
                     config_str += f"            role: {val},\n"
                elif key == 'testId':
                     config_str += f"            testId: '{val}',\n"
                elif key == 'text':
                     config_str += f"            text: '{val}',\n"
                elif key == 'css':
                     config_str += f"            css: '{val}',\n"
                elif key == 'xpath':
                     config_str += f"            xpath: '{val}',\n"
            config_str += "        }"

            code.append(f"    /** {desc} */")
            code.append(f"    get {safe_name}(): Locator {{")
            code.append(f"        return this.smartLocator({config_str});")
            code.append("    }")
            code.append("")

        code.append("    async verifyLoaded() {")
        assertions = model.get("assertions", [])
        if assertions:
            for asn in assertions:
                if "title" in asn.lower():
                    code.append(f"        await expect(this.page).toHaveTitle(/.*{page_name}.*/i);")
                else:
                    code.append(f"        // {asn}")
        else:
            code.append("        await expect(this.page).toHaveURL(/.*$/);")
        code.append("    }")
        code.append("}")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(code))
        print(colored(f"   ✅ Generated {filename} (Smart Locators)", "green"))

    def _guess_strategy(self, locator):
        """Heuristic to map locator string to SmartLocator strategy."""
        # 0. Handle Pre-Generated Playwright Calls (from older models)
        import re
        if ("getByRole" in locator):
            # Extract role and name: getByRole('button', { name: 'Products' })
            match = re.search(r"getByRole\('([^']+)',\s*\{\s*name:\s*'([^']+)'", locator)
            if match:
                return ("role", f"['{match.group(1)}', {{ name: '{match.group(2)}', exact: false }}]")

        if "getByText" in locator:
            # Extract text: getByText('Products')
            match = re.search(r"getByText\('([^']+)'\)", locator)
            if match:
                return ("text", match.group(1))

        # 0.5 Role Detection for links/buttons (heuristic)
        low_loc = locator.lower()
        if "link" in low_loc and not "getByRole" in locator:
             return ("role", f"['link', {{ name: '{locator.replace('link=', '')}' }}]")
        if "button" in low_loc and not "getByRole" in locator:
             return ("role", f"['button', {{ name: '{locator.replace('button=', '')}' }}]")
        
        # 0.7 If locator contains ">" it's often a menu item, prefer text
        if ">" in locator:
            clean_text = locator.split(">")[0].strip()
            return ("text", clean_text)

        locator = locator.replace("'", "\\'") # Escape for TS string

        # 1. XPath
        if locator.startswith("//") or "xpath=" in locator:
            return ("xpath", locator.replace("xpath=", ""))
            
        # 2. CSS (Heuristic)
        if "css=" in locator or locator.startswith(".") or "#" in locator or ">" in locator or "[" in locator:
             return ("css", locator.replace("css=", ""))
             
        # 3. Fallback
        return ("text", locator)

    def _generate_test_file(self):
        """Generates a skeleton for the Refiner to populate."""
        if not os.path.exists(self.trace_path): return
        
        with open(self.trace_path, "r") as f:
            trace_data = json.load(f)
            
        test_filename = "workflow.spec.ts"
        os.makedirs(self.tests_dir, exist_ok=True)
        filepath = os.path.join(self.tests_dir, test_filename)
        
        code = [
            "import { test, expect } from '@playwright/test';",
            "// Page imports will be added by Refiner",
            "",
            "test('Autonomous Workflow', async ({ page }) => {",
            f"    // Target: {trace_data.get('target_url')}",
            "    // Logic delegated to Refiner",
            "});"
        ]
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(code))
        print(colored(f"   ⚠️ Test Generation delegated to Refiner (Smart Mode)", "yellow"))

    def _to_snake_case(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

