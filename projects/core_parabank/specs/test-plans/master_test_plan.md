# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing will cover account access, transfers & payments, and statements & history modules.

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities of the application are working as expected.  It will be executed on every build to quickly identify any major issues.

#### Smoke Suite Strategy

The following 8-point checklist was applied when designing the smoke suite for this project:

<<<<<<< Updated upstream
1.  **Critical Paths:** Tests cover the most essential user workflows (e.g., login).
2.  **Core Business Logic:** Focuses on primary revenue or operational flows.
3.  **Positive Testing:** Primarily happy path scenarios are included.
4.  **No Negative Testing:**  Negative tests are excluded unless critical for security.
5.  **No Complex Edge Cases:** Complex or less common scenarios are avoided.
6.  **Fast Execution:** Tests are designed for quick execution to provide rapid feedback.
7.  **Build Validation:**  A failed smoke test indicates a critical issue, potentially rejecting the build.
8.  **Limited Scope:** The suite is kept small and manageable, focusing on the most vital functions.

### Regression Suite

The regression suite will provide a comprehensive test coverage to ensure that new changes have not introduced any regressions. It will include alternative flows, negative scenarios, boundary analysis, and cross-module interactions.
=======
1.  **Critical Paths:** Tests cover the most important user workflows (e.g., login).
2.  **Core Business Logic:** Focus on primary revenue or operational flows.
3.  **Positive Testing:** Primarily happy path scenarios.
4.  **No Negative Testing:** Unless critical security concerns exist.
5.  **No Complex Edge Cases:** Avoid intricate scenarios in smoke tests.
6.  **Fast Execution:** Tests should be quick to execute.
7.  **Independent Tests:** Tests should not depend on each other.
8.  **Limited Data Dependency:** Minimize reliance on specific test data.

### Regression Suite

The regression suite will provide comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. This suite will be executed periodically to ensure existing functionalities are not broken by new changes.
>>>>>>> Stashed changes

## Test Modules

### Account Access (Criticality: Critical)

*   **Smoke Tests:**
    *   Customer Login
*   **Regression Tests:**
    *   Login with Biometrics/MFA
    *   Recover Forgotten Username/Password
    *   Session Timeout Handling

### Transfers & Payments (Criticality: Critical)

*   **Smoke Tests:**
    *   Internal Fund Transfer (Checking to Savings)
*   **Regression Tests:**
    *   Transfer exceeding balance (Insufficient Funds)
    *   Transfer exceeding daily limit
    *   Schedule Future Date Transfer
    *   Add New Payee/Beneficiary

### Statements & History (Criticality: Medium)

*   **Smoke Tests:**
    *   View Recent Transactions
*   **Regression Tests:**
    *   Download Statement (PDF/CSV)
    *   Search Transactions by Keyword
    *   Filter Transactions by Amount Range
