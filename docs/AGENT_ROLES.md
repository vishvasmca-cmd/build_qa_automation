# Agent Roles & Responsibilities

The Antigravity framework is composed of specialized autonomous agents, each with a distinct responsibility in the testing lifecycle.

---

## 1. Explorer Agent (`core/agents/explorer.py`)
**"The Navigator"**

*   **Role**: Explore the target website autonomously to understand its structure and user flows.
*   **Input**: Target URL, High-level Goal (e.g., "Find the login page").
*   **Output**: `trace.json` (Interaction logs), `snapshots/` (DOM snapshots & Screenshots).
*   **Key Responsibilities**:
    *   Navigate through the application without getting stuck.
    *   Handle pop-ups, modals, and new tabs.
    *   Record user actions (clicks, fills) that achieve the goal.
    *   **Self-Healing**: Detects 404s and loops; attempts to back-track or refresh.

## 2. Batch Miner (`core/agents/miner.py`)
**"The Archaeologist"**

*   **Role**: Analyze static artifacts to discover robust, reusable page models.
*   **Input**: `snapshots/` (HTML/Screenshots) from the Exploration phase.
*   **Output**: `page_models.json` (Structured definition of Pages, Locators, and Assertions).
*   **Key Responsibilities**:
    *   Cluster similar pages (e.g., "Product Details Page").
    *   generate resilient locators (ID > TestID > Role > CSS).
    *   Identify potential assertion points (Page Titles, Success Messages).

## 3. Framework Generator (`core/agents/refiner.py`)
**"The Architect"**

*   **Role**: Convert abstract page models into executable Python code.
*   **Input**: `page_models.json`, `trace.json`.
*   **Output**: `pages/*.py` (Page Objects), `tests/test_main.py` (Test Script).
*   **Key Responsibilities**:
    *   Generate Python classes following the [Standard POM Guide](STANDARD_POM_GUIDE.md).
    *   Ensure strict separation of concerns (Locators vs. Logic).
    *   Write linear, readable test scenarios.

## 4. Pytest Executor (`core/lib/base_page.py` & `orchestrator.py`)
**"The Operator"**

*   **Role**: Execute the generated tests and validate business goals.
*   **Input**: `tests/test_main.py`.
*   **Output**: `report.html`, `test-results/` (Traces), Pass/Fail Status.
*   **Key Responsibilities**:
    *   Run tests in a controlled environment.
    *   **Runtime Self-Healing**: The `BasePage` class automatically intercepts clicks that fail due to overlays and retries with `force=True` or overlay dismissal logic.

## 5. Feedback Agent (`core/agents/feedback_agent.py`)
**"The Critic"**

*   **Role**: Analyze failures and teach the system how to improve.
*   **Input**: Execution Logs, Error Messages, Screenshots of failure.
*   **Output**: Updated `knowledge/failures.json`, Updated `rules.md`.
*   **Key Responsibilities**:
    *   Distinguish between "Bug in App" vs. "Bug in Test".
    *   Update site-specific rules (e.g., "This site is slow, increase timeouts").
    *   Trigger re-generation of code if the logic was flawed.

## 6. Spec Synthesizer (`core/knowledge/spec_synthesizer.py`)
**"The Planner"**

*   **Role**: Translate high-level user intent into detailed technical specifications.
*   **Input**: User Goal, Domain (e.g., "Banking").
*   **Output**: `master_plan` in `config.json`.
*   **Key Responsibilities**:
    *   Determine the necessary test coverage (Smoke vs. Regression).
    *   Break down complex goals into sub-tasks.

## 7. Security Auditor (`core/agents/security_auditor.py`)
**"The Guard"**

*   **Role**: Perform basic security sanity checks on the target.
*   **Input**: Target URL.
*   **Output**: Security Report.
*   **Key Responsibilities**:
    *   Check for exposed headers (e.g., X-Powered-By).
    *   Verify basic SSL/TLS configuration.
    *   (Future) Check for common vulnerabilities like XSS in inputs.
