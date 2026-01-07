# Test Plan: core_parabank

## Overview

This test plan outlines the testing strategy for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing will cover the following modules:

*   Account Access
*   Transfers & Payments
*   Statements & History

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities of the application are working as expected.  If any smoke tests fail, the build should be rejected.

**Smoke Suite Strategy**

The following checklist was applied when designing the smoke suite for this project:

1.  **Critical Paths:** Tests cover the most essential user workflows (e.g., login).
2.  **Core Business Logic:** Focus on primary revenue or operational flows.
3.  **Positive Testing:** Primarily happy path scenarios.
4.  **No Negative Testing:** Avoid negative tests unless critical for security.
5.  **No Complex Edge Cases:** Exclude intricate or less common scenarios.
6.  **Fast Execution:** Tests should be quick to execute for rapid feedback.
7.  **Independent Tests:** Tests should be independent and not rely on each other.
8.  **Limited Scope:** Focus on a minimal set of functionalities.

### Regression Suite

The regression suite will provide a comprehensive test coverage to ensure that new changes have not introduced any regressions in existing functionalities. This suite will include alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

## Test Modules

### Account Access (Criticality: Critical)

*   **Smoke Tests:**
    *   Customer Login
    *   View Account Dashboard
*   **Regression Tests:**
    *   Login with Biometrics/MFA
    *   Recover Forgotten Username/Password
    *   Session Timeout Handling

### Transfers & Payments (Criticality: Critical)

*   **Smoke Tests:**
    *   Internal Fund Transfer (Checking to Savings)
    *   Bill Payment (Standard)
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
