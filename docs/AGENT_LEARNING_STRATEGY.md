# Agent Learning Strategy & Implementation Plan

This document outlines the strategy to transition our agents from "Stateless Execution" to a "Continuous Learning" model to prevent repetitive errors in locators and code generation.

---

## 🏛️ The Learning Architecture

We define three tiers of learning to ensure agents don't repeat the same mistakes:

1.  **Level 1: Reflexive Learning (The "BasePage" Layer)**
    *   **Scope**: Immediate run-time recovery.
    *   **Mechanism**: If a click fails due to an overlay, the `BasePage` immediately triggers `remove_ads()` and retries.
    *   **Goal**: Zero "flaky" failures during stable runs.

2.  **Level 2: Active Self-Correction (The "Agent" Layer)**
    *   **Scope**: Within a single project pipeline.
    *   **Mechanism**: If the `Refiner` generates code with a syntax error, it must "lint" itself, read the error, and fix the code **before** reporting status to the Orchestrator.
    *   **Goal**: Prevent "Attempt 2" from repeating "Attempt 1" syntax errors.

3.  **Level 3: Global Knowledge (The "RAG" Layer)**
    *   **Scope**: Across multiple projects and sessions.
    *   **Mechanism**: The `Feedback Agent` distills failures into `knowledge/failures.json` and updates `rules.md` for specific sites.
    *   **Goal**: Permanent avoidance of site-specific traps (e.g., "Always use `force=True` on Parabank").

---

## 📋 Agent-Specific Learning Curves

### 🧭 Explorer Agent: "Cognitive Navigation"
*   **Current State**: Repeats loops if a button state doesn't change.
*   **Target State**:
    *   **Action Scorecard**: Each action (Click, Fill) is scored. If an action is repeated 3 times with no DOM change, it is marked as "Ineffective" and the agent is forced to ignore that element and pivot.
    *   **Dynamic Rule Reading**: The Explorer will reload `rules.md` at every step, allowing the `Feedback Agent` to "guide" it in real-time during a retry loop.

### ⛏️ Batch Miner: "Stability-First Discovery"
*   **Current State**: Picks locators based on DOM priority.
*   **Target State**:
    *   **Historical Locator Ranking**: Integration with `learned_patterns_v2.json`. If a locator (e.g., `#login`) has failed in the past, the Miner will demote it and prioritize a more stable Playwright role-based selector.
    *   **Auto-Assertion Discovery**: Learns to identify "Progress Indicators" (e.g., "Step 2 of 4") to generate smarter `wait_for` logic.

### 🛠️ Framework Generator (Refiner): "The Linting Loop"
*   **Current State**: Generates code and waits for the Orchestrator to run it.
*   **Target State**:
    *   **Internal Verification**: Before saving `test_main.py`, the Refiner runs `py_compile` or a dry-run import.
    *   **Self-Fixing Prompt**: If the dry-run fails, the Refiner passes the error back to the LLM: *"Your last code failed with IndentationError on line 42. Please fix this and ensure absolute imports are used."*

### 🧠 Feedback Agent: "The Site-Specific Teacher"
*   **Current State**: Writes high-level summaries.
*   **Target State**:
    *   **Context-Injected Extraction**: Instead of just saying "it failed," it will extract the specific selector that failed and write a **Mandatory Rule** to `rules.md`: *"NEVER use the ID 'btn-save' on this site; it is a hidden overlay."*

---

## 📅 Roadmap for Implementation

| Phase | Feature | Target Agent | Priority |
| :--- | :--- | :--- | :--- |
| **Immediate** | **Linting Loop** (Self-fixing syntax) | Refiner | 🔴 High |
| **Short-term** | **Mandatory Rule Injection** | Feedback Agent | 🟡 Med |
| **Medium-term** | **Action Scorecard** (Loop prevention) | Explorer | 🟡 Med |
| **Long-term** | **Global Locator Stability Scores** | Miner | 🟢 Low |

---

**Objective**: By implementing these curves, we ensure that an error encountered in **Attempt 1** is technically impossible to repeat in **Attempt 2**.
