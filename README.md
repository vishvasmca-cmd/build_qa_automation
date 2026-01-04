# 🤖 Antigravity - Autonomous Test Generation Framework

## 🚀 **Single Command Entry Point**

```bash
python run.py --project <name> --url <url> --goal <goal> --domain <auto|banking|ecommerce|saas|isp_telecom>
```

---

## 📋 **Quick Start Examples**

### **Auto-Detect Domain & Generate Tests**
```bash
python run.py \
  --project my_test \
  --url "https://any-website.com" \
  --goal "User registration" \
  --domain auto
```
✅ Automatically detects domain  
✅ Mines page elements  
✅ Generates working Playwright tests  
✅ Executes and validates  

### **Generate Comprehensive Spec First**
```bash
python run.py \
  --project banking_test \
  --url "https://parabank.parasoft.com/parabank/" \
  --goal "Fund transfer" \
  --domain auto \
  --generate-spec
```
✅ Auto-detects domain (Banking)  
✅ Generates domain-specific test scenarios  
✅ Creates spec files  
✅ Runs autonomous exploration  

---

## 🏗️ **Architecture Overview**

```
run.py (MAIN ENTRY POINT)
  │
  ├─► Domain Detection (if --domain auto)
  │
  ├─► Spec Generation (if --generate-spec)
  │
  └─► Orchestrator Pipeline
      │
      ├─► [Step 1] Predictive QA (RAG Context)
      │   ├─ Query Knowledge Bank (knowledge_bank.py)
      │   ├─ Check 'next_action_prediction.jsonl'
      │   └─ Inject "Best Next Steps" into Prompt
      │
      ├─► [Step 2] Explorer (core/explorer.py)
      │   ├─ AI-powered navigation
      │   ├─ Fail-Fast on 404
      │   └─ Outputs: trace.json
      │
      ├─► [Step 3] Knowledge Aggregation (core/data_aggregator.py)
      │   ├─ Parse trace.json
      │   ├─ Create training datasets (*.jsonl)
      │   └─ Update 'learned_patterns_v2.json'
      │
      ├─► [Step 4] Code Generation (core/refiner.py)
      │   ├─ Trace → Playwright Monolith
      │   └─ Outputs: tests/test_main.py
      │
      └─► [Step 5] Test Execution
          ├─ pytest with retries
          └─ Self-healing on failures
```

---

## 📁 **Project Structure**

inner-event/
├── run.py                          ⭐ SINGLE ENTRY POINT
├── core/
│   ├── orchestrator.py             # Pipeline controller
│   ├── explorer.py                 # AI navigation agent
│   ├── data_aggregator.py          # 🧠 Knowledge Aggregation
│   ├── refiner.py                  # Test code generation
│   ├── knowledge_bank.py           # RAG & Predictive Context
│   └── ...
│
├── knowledge/                      # Knowledge Bank (RAG)
│   ├── learned_patterns_v2.json    # Stable Locators
│   └── datasets/                   # Training Data
│       └── next_action_prediction.jsonl
│
└── projects/                       # Generated test projects
    ├── {project_name}/
    │   ├── config.json             # Project configuration
    │   ├── outputs/
    │   │   ├── trace.json          # Exploration log
    │   │   └── report.html         # Visual report
    │   ├── tests/
    │   │   └── test_main.py        # 🚀 Monolithic Self-Contained Test
    │   └── specs/
    │       └── test-plans/         # Strategy documents

---

## 🎯 **Core Features**

### **1. Automatic Domain Detection**
```python
# In run.py lines 12-75
async def detect_and_generate_spec(url, project_name):
    # Analyzes: Title, Navigation, Content
    # Classifies: E-commerce, Banking, SaaS, ISP, Healthcare, etc.
    # Returns: domain string
```

**Supported Domains**:
- ✅ E-commerce (Products, Cart, Checkout)
- ✅ Banking (Accounts, Transfers, Compliance)
- ✅ SaaS (Dashboards, CRUD, Subscriptions)
- ✅ ISP/Telecom (Bills, Service Plans, Support)
- ✅ Healthcare (Patient Portals, HIPAA)
- ✅ Education (LMS, Courses)
- ✅ Government (Public Services)
- ✅ Social Media (Feeds, Messaging)

### **2. Intelligent Explorer** (`core/explorer.py`)

**Key Capabilities**:
- ✅ **Autonomous Navigation**: AI decides next action
- ✅ **Fail-Fast Intelligence**: Detects 404s/DNS errors & aborts immediately
- ✅ **Multi-Tab Handling**: Switches to new windows automatically
- ✅ **Autonomous Registration**: Detects "no credentials" → finds Sign Up → registers
- ✅ **Multi-Method Scrolling**: Keyboard + Mouse + JS for element discovery
- ✅ **Test Data Extraction**: Finds credentials on page → persists to `test_data.json`
- ✅ **Self-Healing**: Auto-repairs broken locators during execution

**Production Site Support**:
- 60s page load timeout
- Lazy loading detection
- Network idle optional (skips if timeout)

### **3. Predictive QA (RAG)** (`core/knowledge_bank.py`)

**How it works**:
1.  **Ingest**: Reads `knowledge/datasets/next_action_prediction.jsonl`.
2.  **Match**: Uses fuzzy logic + domain matching to find similar past goals.
3.  **Predict**: Injects "Best Next Step" into the Agent's context.

**Benefit**: Prevents the agent from repeating past mistakes (e.g., "Don't click X, click Y instead").

### **4. Knowledge Aggregation** (`core/data_aggregator.py`)

**Command**:
```bash
python core/data_aggregator.py
```
**Function**:
- Scans all `projects/*/outputs/trace.json`.
- Extracts successful action sequences.
- Compiles them into training datasets for:
    - Next Action Prediction
    - Locator Prediction

### **5. Code Generation** (`core/refiner.py`)

**Philosophy**: **Autonomous Monolith**
- We generate single-file, self-contained tests (`test_main.py`).
- No complex Page Object Model (POM) dependencies.
- **Why?** Easier for AI to read, debug, and self-heal a single file than a distributed class hierarchy.

**Generated Test Includes**:
```python
def smart_action(page, locator, action, value):
    # Self-healing wrapper
    # Auto-retries with fallback selectors
    
def test_autonomous_flow(page):
    # End-to-End User Flow
```

### **6. Comprehensive Reporting** (`core/reporter.py`)

**Outputs**:
- `report.html` - Beautiful HTML with screenshots
- `report.md` - Markdown summary
- `screenshots/` - Visual evidence of every step

---

## 🔧 **Configuration**

### **Project Config** (`projects/{name}/config.json`)
```json
{
  "project_name": "my_test",
  "target_url": "https://example.com",
  "workflow_description": "User registration",
  "domain": "ecommerce",
  "test_data": {
    "username": "user@example.com",
    "password":  "SecurePass123"
  },
  "paths": {
    "trace": "projects/my_test/outputs/trace.json",
    "report": "projects/my_test/outputs/report.md",
    "test": "projects/my_test/tests/test_main.py"
  }
}
```

### **Environment Variables**
```bash
# .env file
GOOGLE_API_KEY=your_gemini_api_key
```

---

## 🚦 **Usage Patterns**

### **Pattern 1: Quick Test Generation**
```bash
python run.py --project demo --url https://demo.site --goal "Login" --domain auto
```
**Use when**: Testing a new site quickly

### **Pattern 2: Comprehensive Spec-Driven**
```bash
python run.py --project prod --url https://prod.site --goal "Checkout" --domain auto --generate-spec
```
**Use when**: Production testing, need detailed scenarios

### **Pattern 3: Manual Domain**
```bash
python run.py --project bank --url https://bank.com --goal "Transfer" --domain banking
```
**Use when**: You know the domain, skip detection

---

## 🐛 **Troubleshooting**

### **Timeout Errors**
**Issue**: `Timeout 30000ms exceeded`  
**Fix**: Increased to 60s in `core/explorer.py` line 94, 104

### **Login Failures**
**Issue**: Agent skips login or uses wrong credentials  
**Fix**: Update `projects/{name}/config.json` test_data section

### **Missing Login Button Click**
**Issue**: Fills username/password but doesn't submit  
**Fix**: Check trace.json - may need to adjust decision prompt

### **JS vs Python Locators**
**Issue**: `getByRole` instead of `get_by_role`  
**Fix**: Auto-converted in `core/explorer.py` lines 265-270

---

## 📚 **Training & Knowledge**

**Pre-trained Sites**:
- ✅ www.saucedemo.com (E-commerce)
- ✅ parabank.parasoft.com (Banking)
- ✅ webdriveruniversity.com (Tutorial)
- ✅ the-internet.herokuapp.com (Edge cases)

**To add new knowledge**:
```bash
python run.py --project new_site --url https://new.site --goal "Main workflow" --domain auto
# Knowledge auto-updates in knowledge/sites/
```

---

## 🎨 **Key Learnings Implemented**

1. **Language Syntax War**: Auto-converts JS → Python Playwright
2. **Multi-Tab Navigation**: Detects + switches to new windows
3. **Form Field Intelligence**: Distinguishes inputs from submit buttons
4. **Sequential Form Filling**: One field at a time, validates before submit
5. **Autonomous Registration**: No hardcoded credentials needed
6. **Error Resilience**: All code paths return consistent dicts
7. **Multi-Method Scrolling**: 3 techniques for element discovery
8. **Knowledge Evolution**: Locator stability + domain patterns

---

## 🚀 **Next Steps**

1. **Run first test**:
   ```bash
   python run.py --project first_test --url https://example.com --goal "Explore" --domain auto
   ```

2. **Check outputs**:
   ```bash
   explorer projects\first_test\outputs\report.html
   ```

3. **Run generated test**:
   ```bash
   pytest projects/first_test/tests/test_main.py
   ```

4. **Iterate**: Update config → re-run → refine

---

## 🔮 **Future Roadmap**

### **1. Offline Model Fine-Tuning**
*   **Goal**: Create a specialized "QA-Agent-7B" model.
*   **Method**: Use the `knowledge/datasets/next_action_prediction.jsonl` dataset (generated by the Data Aggregator) to fine-tune Llama 3 or Mistral.
*   **Result**: An LLM that understands "Test Automation" natively, reducing token costs and increasing accuracy.

### **2. Visual Grounding**
*   **Goal**: Enable the agent to "see" the page layout.
*   **Method**: Integrate Gemini Pro Vision or GPT-4o to analyze screenshots for layout issues (overlapping text, broken images) and visual locators.

### **3. Parallel Sharding**
*   **Goal**: Execute 100 tests in 5 minutes.
*   **Method**: Use `pytest-xdist` to run the self-contained monolithic tests in parallel worker nodes.

---

## 📖 **Further Reading**

- `UNIVERSAL_SPEC_GUIDE.md` - Domain detection details
- `BANKING_TESTS_README.md` - Banking-specific examples
- `knowledge/domains/*.yaml` - Domain patterns

---

**Built with**: Gemini 2.0 Flash, Playwright, Python  
**Status**: Production-ready for web testing automation  
**License**: MIT
