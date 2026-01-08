# System Workflow Diagram

This document illustrates the end-to-end flow of the Antigravity Autonomous QA Framework.

```mermaid
graph TD
    User([User / CI Trigger]) -->|Config + URL| Orchestrator{Orchestrator}
    
    subgraph "Phase 1: Knowledge & Planning"
        Orchestrator -->|Query| KnowledgeBank[Knowledge Bank]
        KnowledgeBank -->|Context & Rules| Orchestrator
        Orchestrator -->|Context| Planner[Spec Synthesizer]
        Planner -->|Master Plan| Orchestrator
    end

    subgraph "Phase 2: Exploration & Mining"
        Orchestrator -->|Plan| Explorer[Explorer Agent]
        Explorer -->|Navigates Site| Website(Target Website)
        Explorer -->|Snapshots & Trace| Artifacts[(Artifacts)]
        
        Artifacts -->|Input| Miner[Batch Miner]
        Miner -->|Discover Elements| PageModels[Page Models JSON]
    end

    subgraph "Phase 3: Code Generation"
        PageModels -->|Blueprint| Generator[Framework Generator]
        Generator -->|Create| POM[Page Objects]
        Generator -->|Create| Tests[Pytest Scripts]
    end

    subgraph "Phase 4: Execution & Healing"
        Orchestrator -->|Run| Executor[Pytest Executor]
        Executor -->|Execute| Tests
        Tests -->|Interact| Website
        
        Executor -- Success --> Report[HTML Report]
        Executor -- Failure --> Feedback[Feedback Agent]
        
        Feedback -->|Analyze Error| KnowledgeBank
        Feedback -->|Update Rules| KnowledgeBank
        Feedback -->|Retry Instuction| Orchestrator
    end

    style Orchestrator fill:#f9f,stroke:#333,stroke-width:2px
    style Website fill:#ccf,stroke:#333
    style Artifacts fill:#ff9,stroke:#333
    style KnowledgeBank fill:#9f9,stroke:#333
```

## Workflow Description

1.  **Trigger**: The process starts with `trigger_agent.py` receiving a target URL and project configuration.
2.  **Planning**: The `SpecSynthesizer` creates a high-level plan based on the goal (e.g., "Checkout Flow").
3.  **Exploration**: The `Explorer Agent` navigates the live site, capturing DOM snapshots and user interactions.
4.  **Mining**: The `Batch Miner` processes offline snapshots to identify strictly consistent locators and page structures.
5.  **Generation**: The `Framework Generator` builds a standardized Page Object Model (POM) and linear test scripts.
6.  **Execution**: `Pytest` executes the generated tests.
7.  **Self-Healing**: If execution fails, the `Feedback Agent` diagnoses the root cause (e.g., "Modal blocked click"), updates the `Knowledge Bank`, and triggers a retry or regeneration.
