# 🏗️ Architecture Deep Dive - run.py Framework

## 📍 **Core Design Principles**

1. **Single Entry Point**: All functionality accessible via `run.py`
2. **Domain-Aware**: Auto-detects site type for intelligent testing
3. **Self-Healing**: Tests auto-repair broken locators
4. **Knowledge Accumulation**: learns from every run (RAG)
5. **Production-Ready**: Handles timeouts, multi-tabs, slow sites

---

## 🔄 **Execution Flow**

```
USER COMMAND
    ↓
run.py main()
    ├─ Parse arguments (--project, --url, --goal, --domain)
    ├─ Create project workspace
    │
    ├─ [OPTIONAL] Domain Detection
    │   ├─ Launch headless browser
    │   ├─ Extract: title, nav, content
    │   ├─ LLM classification
    │   └─ Store detected domain
    │
    ├─ [OPTIONAL] Spec Generation
    │   ├─ Domain-specific prompt
    │   ├─ LLM generates test scenarios
    │   └─ Save to projects/{name}/specs/
    │
    ├─ Create/Update config.json
    │   └─ test_data, paths, domain
    │
    └─ run_pipeline(config_path)
        ↓
core/orchestrator.py
    ├─ Step 1: explorer.explore()
    ├─ Step 2: knowledge_bank.update_from_run()
    ├─ Step 3: refiner.generate_code_from_trace()
    ├─ Step 4: reporter.generate_report()
    └─ Step 5: pytest execution
```

---

## 🧩 **Component Breakdown**

### **1. run.py** (Main Entry)

**Location**: `c:/Users/vishv/.gemini/antigravity/playground/inner-event/run.py`

**Key Functions**:

```python
async def detect_and_generate_spec(url, project_name):
    """
    Auto-detect domain using browser + LLM
    Args:
        url: Target website
        project_name: Project identifier
    Returns:
        domain: str (e.g., "ecommerce", "isp_telecom")
    """
    # 1. Launch Playwright browser (headless)
    # 2. Extract page metadata (title, nav, content)
    # 3. LLM classifies domain
    # 4. Returns domain string

def generate_spec_files(url, project_name, domain):
    """
    Generate domain-specific test scenarios
    Args:
        domain: Detected domain type
    Outputs:
        projects/{name}/specs/test_spec.json
    """
    # 1. Domain-aware LLM prompt
    # 2. Generates workflows, scenarios, edge cases
    # 3. Saves JSON spec

def main():
    """
    Unified entry point
    Flow:
        Parse args → Detect domain → Generate spec → Run pipeline
    """
```

**Arguments**:
- `--project` (required): Project name
- `--url`: Target URL (required for new projects)
- `--goal`: Test objective
- `--domain`: auto | ecommerce | banking | saas | isp_telecom
- `--generate-spec`: Flag to create comprehensive specs
- `--docs`: Additional instructions

**Design Decisions**:
- **Why async domain detection?** Playwright requires async context
- **Why optional spec generation?** Fast iteration vs comprehensive planning
- **Why default domain="auto"?** User convenience

---

### **2. core/explorer.py** (AI Navigator)

**Purpose**: Autonomously navigate websites and mine elements

**Key Methods**:

```python
class ExplorerAgent:
    async def explore(self):
        """
        Main exploration loop
        Flow:
            1. goto(url, timeout=60s)  # Longer for production
            2. while step_count < max_steps:
                a. wait_for_load_state (optional timeout catch)
                b. analyze_page (miner.py)
                c. _decide_action (LLM reasoning)
                d. _execute_action
                e. Switch to new_page if tab opened
            3. _save_trace()
        """
    
    def _decide_action(self, page_summary, elements, history):
        """
        LLM decision-making
        Inputs:
            - Page context
            - Available elements
            - Action history
            - test_data (credentials)
        Output:
            {
                "thought": "...",
                "action": "click | fill | scroll | done",
                "target_element_id": "el_0",
                "value_to_fill": "...",
                "scroll_direction": "down | up"
            }
        """
    
    async def _execute_action(self, page, decision, locators):
        """
        Execute the decided action
        Returns:
            {"locator": str, "new_page": Page | None}
        
        Handles:
            - Multi-tab detection (page.context.expect_page)
            - Scroll (PageDown, MouseWheel, ScrollIntoView)
            - Click with new tab capture
            - Fill with validation
        """
```

**Critical Fixes**:
- **Line 94**: `timeout=60000` for slow production sites
- **Line 104**: Optional networkidle (catches timeout, continues)
- **Line 196-215**: Scroll action with multiple methods
- **Line 270-310**: New tab detection + switching

**Prompt Engineering**:
```python
SYSTEM_PROMPT_DECIDER = """
Rules:
1. REGISTRATION FORMS: Never click Submit until ALL fields filled
2. Fill fields ONE AT A TIME in sequence
3. Check VALUES: Don't re-fill if already correct
4. SCROLLING: Use to discover more elements
"""
```

---

### **3. core/miner.py** (Element Extractor)

**Purpose**: Extract DOM elements and classify them

**Key Functions**:

```python
async def analyze_page(page, url, knowledge_context, cache_path, force_refresh):
    """
    Extracts interactive elements from page
    Flow:
        1. extract_dom_snapshot() - JS execution
        2. Check cache (skip if force_refresh)
        3. _get_page_summary() - LLM summarizes page
        4. _mine_interactive_elements() - LLM proposes locators
        5. Save cache (hash-based)
    Returns:
        {
            "summary": {...},
            "locators": [...]
        }
    """

async def extract_dom_snapshot(page):
    """
    JavaScript execution in browser
    Returns:
        {
            "interactables": [
                {
                    "id": "el_0",
                    "tag": "input",
                    "type": "text",
                    "name": "username",
                   "placeholder": "Enter username",
                    "value": "",
                    "testId": "...",
                    "customTestId": "data-test value"
                }
            ],
            "bodyText": "Page content sample"
        }
    """
```

**Design Decisions**:
- **Why cache?** Avoid re-mining unchanged pages (expensive LLM calls)
- **Why hash-based cache?** Detect subtle DOM changes
- **Why `type` and `name` metadata?** Distinguish form fields from submit buttons

**Locator Prioritization**:
1. `data-test` (most stable)
2. `data-testid`
3. `input[name='...']` (for forms)
4. `get_by_role` with name
5. CSS/XPath fallback

---

### **4. core/refiner.py** (Code Generator)

**Purpose**: Convert trace → executable Playwright test

**Key Function**:

```python
def generate_code_from_trace(trace, config_path):
    """
    Inputs:
        trace: List of {page_name, action, locator, value}
        config: Project configuration
    Outputs:
        tests/test_main.py - Executable pytest
    
    Process:
        1. Filter trace (remove duplicate pages)
        2. LLM prompt with strict Python syntax rules
        3. Inject smart_action() helper
        4. Inject take_screenshot() utility
        5. Add assertions (URL, element visibility)
        6. Write to file (UTF-8)
    """
```

**Template Structure**:
```python
# Part 1: Imports
import pytest, os, re
from playwright.sync_api import Page, expect

# Part 2: Helper Functions
def smart_action(page, locator, action, value):
    # Self-healing logic
    # Converts JS → Python locators
    # Retries with fallback selectors

def take_screenshot(page, name):
    # Consistent naming: step_0.png, step_1.png
    
# Part 3: Generated Test
def test_autonomous_flow(page: Page):
    page.goto("...")
    smart_action(page, "locator", "click", None)
    take_screenshot(page, "step_0")
    expect(page).to_have_url("...")
```

**Critical Prompt Rules**:
```
- PYTHON SYNTAX ONLY (not JavaScript)
- Use snake_case: get_by_role (not getByRole)
- Keyword arguments: name="Login" (not { name: 'Login' })
- For inputs, use: input[name='firstName']
- NO JavaScript regex literals (/pattern/)
```

**Self-Healing Logic**:
```python
try:
    # Primary locator
    loc = page.locator(primary_locator)
    loc.click()
except:
    # Fallback: Search all [data-test], button, a
    for el in page.query_selector_all('[data-test], button, a'):
        if keyword in el.text.lower():
            el.click() # Healed!
```

---

### **5. core/knowledge_bank.py** (RAG Storage)

**Purpose**: Long-term learning across test runs

**Structure**:
```python
class KnowledgeBank:
    def __init__(self):
        self.sites = {}  # Site-specific knowledge
        self.domains = {}  # Cross-site patterns
        self.common_flows = {}  # Universal workflows
    
    def get_rag_context(self, url, workflow):
        """
        Returns context to inject into LLM prompts
        Example:
            "For E-commerce sites, cart is usually top-right.
             Login typically requires email + password.
             Stable locator: [data-test='shopping-cart-link']"
        """
    
    def update_from_run(self, url, trace, success):
        """
        Learn from test execution
        If success:
            - Increment locator stability scores
            - Store proven selectors
            - Update domain patterns
        """
    
    def export_knowledge(self, filename):
        """
        Save for versioning/sharing
        Output: JSON with all learned patterns
        """
```

**Storage Format**:
```yaml
# knowledge/sites/www.saucedemo.com/meta.yaml
domain: ecommerce
features:
  - product_catalog
  - shopping_cart
  - checkout_flow
stable_locators:
  login_username:
    selector: "[data-test='username']"
    stability: 10  # Used 10 times successfully
    last_verified: 2026-01-01
```

---

### **6. core/orchestrator.py** (Pipeline Coordinator)

**Purpose**: Execute the 5-step pipeline

**Flow**:
```python
def run_pipeline(config_path):
    config = load_config(config_path)
    
    # Step 1: Explore
    explorer = ExplorerAgent(config_path)
    trace = asyncio.run(explorer.explore())
    
    # Step 2: Update Knowledge
    kb = KnowledgeBank()
    kb.update_from_run(config['target_url'], trace, success=True)
    
    # Step 3: Generate Code
    test_path = refiner.generate_code_from_trace(trace, config_path)
    
    # Step 4: Generate Report
    reporter.generate_report(trace, config)
    
    # Step 5: Execute Test
    result = subprocess.run(['pytest', test_path, '-v'])
    
    # Retry logic (up to 2 attempts)
    if result.returncode != 0:
        retry_with_healing()
```

---

## 🎛️ **Configuration Management**

### **Project Config**
**Location**: `projects/{name}/config.json`

```json
{
  "project_name": "example",
  "target_url": "https://example.com",
  "workflow_description": "User login and checkout",
  "docs": "Use test account: test@example.com",
  "domain": "ecommerce",  // Auto-detected or manual
  "test_data": {
    "username": "test@example.com",
    "password": "Pass123"
  },
  "paths": {
    "trace": "projects/example/outputs/trace.json",
    "report": "projects/example/outputs/report.html",
    "test": "projects/example/tests/test_main.py",
    "cache": "projects/example/knowledge/locator_cache.json"
  }
}
```

**Why this structure?**
- **`test_data`**: Explorer injects into fill actions
- **`paths`**: Consistent file locations
- **`domain`**: Enables domain-specific logic
- **`docs`**: Manual instructions to LLM

---

## 🔐 **Security & Production**

### **Credential Handling**
- Stored in `config.json` (project-specific)
- Never committed to git (add to `.gitignore`)
- Extracted from pages when possible

### **Production Site Considerations**
- 60s page load timeout
- Network idle optional (lazy loading)
- Headless mode (set `headless=False` for debugging)

---

## 🧪 **Testing Strategy**

### **Generated Test Structure**
```python
def test_autonomous_flow(page):
    # 1. Navigation
    page.goto(URL)
    
    # 2. Actions with healing
    smart_action(page, locator, "fill", value)
    
    # 3. Visual proof
    take_screenshot(page, "step_N")
    
    # 4. Assertions
    expect(page).to_have_url(expected_url)
```

### **Pytest Execution**
```bash
pytest projects/{name}/tests/test_main.py -v --headed
```

**Flags**:
- `-v`: Verbose output
- `--headed`: Show browser
- `--slowmo=500`: Slow down actions

---

## 📊 **Performance**

**Typical Run Times**:
- Domain detection: 10-15s
- Exploration (10 steps): 30-60s
- Code generation: 5-10s
- Test execution: 20-30s
- **Total**: 1-2 minutes

**Bottlenecks**:
- Page load times (production sites)
- LLM inference (Gemini API)
- Network idle waits

**Optimizations**:
- Cache mined elements
- Skip domain detection (use manual)
- Reduce max_steps in explorer

---

## 🔮 **Future Enhancements**

1. **Visual AI**: Screenshot-based element detection
2. **API Testing**: Extend to REST/GraphQL
3. **Mobile Support**: Playwright mobile emulation
4. **CI/CD Integration**: GitHub Actions templates
5. **Multi-browser**: Firefox, WebKit support
6. **Parallel Execution**: pytest-xdist integration

---

**Last Updated**: 2026-01-01  
**Version**: 1.0  
**Maintainer**: Vishvas
