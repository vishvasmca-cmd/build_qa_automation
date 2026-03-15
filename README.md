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
  │   ├─ Browser automation analyzes site
  │   ├─ LLM classifies domain
  │   └─ Returns: ecommerce | banking | saas | isp_telecom | etc.
  │
  ├─► Spec Generation (if --generate-spec)
  │   ├─ Domain-aware test scenario generation
  │   ├─ Security/compliance checks
  │   └─ Saves to: projects/{name}/specs/
  │
  └─► Orchestrator Pipeline
      │
      ├─► [Step 1] Explorer (core/explorer.py)
      │   ├─ AI-powered navigation
      │   ├─ Multi-tab handling
      │   ├─ Autonomous registration
      │   └─ Outputs: trace.json
      │
      ├─► [Step 2] Knowledge Bank Update (core/knowledge_bank.py)
      │   ├─ Locator stability tracking
      │   ├─ Domain pattern storage
      │   └─ Outputs: knowledge/sites/{domain}/
      │
      ├─► [Step 3] Code Generation (core/refiner.py)
      │   ├─ Trace → Playwright test
      │   ├─ Self-healing wrappers
      │   ├─ Screenshot utilities
      │   └─ Outputs: tests/test_main.py
      │
      ├─► [Step 4] Report Generation (core/reporter.py)
      │   ├─ HTML + Markdown reports
      │   ├─ Screenshot embedding
      │   └─ Outputs: outputs/report.html
      │
      └─► [Step 5] Test Execution
          ├─ pytest with retries
          ├─ Self-healing on failures
          └─ Final status code
```

---

## 📁 **Project Structure**

```
inner-event/
├── run.py                          ⭐ SINGLE ENTRY POINT
├── core/
│   ├── orchestrator.py             # Pipeline controller
│   ├── explorer.py                 # AI navigation agent
│   ├── miner.py                    # DOM element extraction
│   ├── refiner.py                  # Test code generation
│   ├── reporter.py                 # HTML/MD report creation
│   ├── knowledge_bank.py           # RAG knowledge storage
│   ├── spec_generator.py           # Domain-specific specs (deprecated)
│   └── universal_spec_generator.py # Auto-domain detection (deprecated)
│
├── knowledge/                      # Knowledge Bank (RAG)
│   ├── domains/
│   │   ├── ecommerce.yaml          # E-commerce patterns
│   │   ├── isp_telecom.yaml        # ISP/Telecom patterns
│   │   └── banking.yaml            # Banking patterns
│   └── sites/
│       ├── www.saucedemo.com/
│       │   ├── locators.json       # Stable selectors
│       │   └── meta.yaml           # Site metadata
│       └── parabank.parasoft.com/
│
└── projects/                       # Generated test projects
    ├── {project_name}/
    │   ├── config.json             # Project configuration
    │   ├── outputs/
    │   │   ├── trace.json          # Exploration log
    │   │   ├── report.html         # Visual report
    │   │   └── report.md           # Summary
    │   ├── tests/
    │   │   └── test_main.py        # Executable test
    │   ├── screenshots/
    │   │   └── step_*.png          # Visual proof
    │   ├── specs/                  # (if --generate-spec)
    │   │   └── test_spec.json      # Test scenarios
    │   └── knowledge/
    │       └── locator_cache.json  # Mined elements
```

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
- ✅ **Multi-Tab Handling**: Switches to new windows automatically
- ✅ **Autonomous Registration**: Detects "no credentials" → finds Sign Up → registers
- ✅ **Multi-Method Scrolling**: Keyboard + Mouse + JS for element discovery
- ✅ **Test Data Extraction**: Finds credentials on page → persists to `test_data.json`
- ✅ **Self-Healing**: Auto-repairs broken locators during execution

**Production Site Support**:
- 60s page load timeout
- Lazy loading detection
- Network idle optional (skips if timeout)

### **3. Knowledge Bank (RAG)** (`core/knowledge_bank.py`)

**Storage**:
```
knowledge/
├── domains/{domain}.yaml       # Universal patterns
└── sites/{domain}/
    ├── locators.json           # Proven selectors
    └── meta.yaml               # Site metadata
```

**Features**:
- Locator stability scoring
- Cross-site pattern recognition
- Export for versioning
- RAG context injection into prompts

### **4. Code Generation** (`core/refiner.py`)

**Generated Test Includes**:
```python
def smart_action(page, locator, action, value):
    # Self-healing wrapper
    # Auto-retries with fallback selectors
    
def take_screenshot(page, name):
    # Consistent screenshot naming
    
def test_autonomous_flow(page):
    # Your generated test
    # Step-by-step with assertions
```

**Key Features**:
- Python syntax enforcement (no JS leakage)
- Self-healing locators
- Screenshot after every action
- Smart assertions based on context

### **5. Comprehensive Reporting** (`core/reporter.py`)

**Outputs**:
- `report.html` - Beautiful HTML with screenshots
- `report.md` - Markdown summary
- Screenshots linked in report

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

## 📖 **Further Reading**

- `UNIVERSAL_SPEC_GUIDE.md` - Domain detection details
- `BANKING_TESTS_README.md` - Banking-specific examples
- `knowledge/domains/*.yaml` - Domain patterns

---

**Built with**: Gemini 2.0 Flash, Playwright, Python  
**Status**: Production-ready for web testing automation  
**License**: MIT
