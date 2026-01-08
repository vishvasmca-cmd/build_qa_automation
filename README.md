# 🤖 Antigravity - Autonomous Agentic QA Framework

**Antigravity** is a next-generation autonomous testing framework that uses LLM-powered agents to plan, explore, mine, and generate self-healing E2E tests.

---

## 🚀 **Quick Start**

### **1. Setup Environment**
```bash
pip install -r requirements.txt
playwright install
```

### **2. Run an Autonomous Agent**
The entry point is `trigger_agent.py`, which launches the orchestration pipeline.

```bash
# Run with a specific configuration file (HEADED mode by default)
python trigger_agent.py projects/automationexercise_regression/config.json

# Run in HEADLESS mode
python trigger_agent.py projects/automationexercise_regression/config.json --headless
```

---

## 🔥 **Key Features**

### **1. Autonomous Exploration & Mining**
The **Explorer Agent** (`core/agents/explorer.py`) navigates websites autonomously, discovering interactive elements (buttons, inputs, links) and mapping user flows.
- **Batch Mining**: After exploration, the **Miner** (`core/agents/miner.py`) analyzes the collected snapshots to discover reusable "Page Models".
- **Documentation**: Automatically generates `Navigate.md` (step-by-step path) and `workflow.md` (high-level summary).

### **2. Structure-First POM Generation**
The framework enforces a strict **Page Object Model (POM)** architecture.
- **Generator**: Uses `core/agents/refiner.py` to convert discovered Page Models into Python classes in `pages/`.
- **Standardization**: Adheres to `docs/STANDARD_POM_GUIDE.md` for consistent coding style.
- **Linear Tests**: Generates clean, linear `test_main.py` files that are easy to read and debug.

### **3. Self-Healing Knowledge Bank**
- **RAG-Powered**: The **Knowledge Bank** (`core/knowledge/knowledge_bank.py`) remembers past failures and successful strategies.
- **Feedback Loop**: If a test fails, the **Feedback Agent** (`core/agents/feedback_agent.py`) analyzes the error, updates `knowledge/failures.json`, and refines the agent's rules (`rules.md`) for future runs.

### **4. Robust Orchestration**
The **Master Orchestrator** (`core/engine/orchestrator.py`) manages the entire lifecycle:
1.  **Planning**: Strategy generation.
2.  **Exploration**: Live site mapping.
3.  **Mining**: Static analysis of snapshots.
4.  **Framework Gen**: Creating POM files.
5.  **Execution**: Running Pytest with self-correction.
6.  **Reporting**: Generating HTML reports and dashboards.

---

## 📁 **Project Structure**

The codebase is organized into logical layers:

```text
inner-event/
├── trigger_agent.py                # 🚀 Entry Point
├── core/                           # Framework Core
│   ├── agents/                     # Autonomous Agents
│   │   ├── explorer.py             # Navigation & Discovery
│   │   ├── miner.py                # Batch DOM Analysis
│   │   ├── refiner.py              # Code Generation
│   │   ├── feedback_agent.py       # Failure Analysis
│   │   └── ...
│   ├── engine/                     # Orchestration Logic
│   │   ├── orchestrator.py         # Main Pipeline Controller
│   │   └── dispatcher.py           # Task Routing
│   ├── knowledge/                  # RAG & Memory
│   │   ├── knowledge_bank.py       # Vector/Rule Store
│   │   └── knowledge_curator.py    # Data Management
│   └── lib/                        # Shared Utilities
│       ├── dom_driver.py           # Playwright Wrapper
│       ├── llm_utils.py            # AI Model Interface
│       └── metrics_logger.py       # Telemetry
│
├── projects/                       # User Projects
│   └── {project_name}/
│       ├── config.json             # Project Config
│       ├── pages/                  # Generated Page Objects
│       ├── tests/                  # Generated Tests
│       └── outputs/                # Artifacts
│           ├── test-results/       # Playwright Traces/Videos
│           ├── snapshots/          # Exploration Screenshots
│           └── report.html         # Final Report
│
└── docs/                           # Documentation
    └── STANDARD_POM_GUIDE.md       # Coding Standards
```

---

## 🔧 **Configuration**

Each project is defined by a `config.json` file:

```json
{
  "project_name": "automationexercise_regression",
  "target_url": "https://automationexercise.com",
  "workflow_description": "User registration and checkout flow",
  "domain": "ecommerce",
  "test_data": {
    "username": "test@example.com",
    "password": "Password123"
  },
  "browser_config": {
    "viewport": { "width": 1280, "height": 720 },
    "headless": false
  }
}
```

---

## 📊 **Reporting**

After a run, check the project's output directory:

- **HTML Report**: `projects/{name}/outputs/report.html`
- **Playwright Trace**: `projects/{name}/outputs/test-results/` (Use `playwright show-trace`)
- **Navigation Log**: `projects/{name}/outputs/Navigate.md`

---

**Built with**: Gemini 2.0 Flash, Playwright, Python
**Status**: Production-Ready
