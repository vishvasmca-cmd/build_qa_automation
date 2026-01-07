# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing will cover the following modules:

*   Account Access
*   Transfers & Payments
*   Statements & History

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities of the application are working as expected. This suite will be executed for every build to quickly identify any major issues.

#### Smoke Suite Strategy

The following 8-point checklist is applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover the most essential user workflows (e.g., login).
2.  **Core Business Logic:** Focus on primary revenue or operational flows.
3.  **Positive Testing:** Primarily happy path scenarios are included.
4.  **No Negative Testing:** Negative tests are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex or less common scenarios are not included.
6.  **Fast Execution:** Tests are designed for quick execution to provide rapid feedback.
7.  **Build Validation:** Failure of any smoke test indicates a critical issue, potentially rejecting the build.
8.  **Limited Scope:** The suite is kept small and manageable, focusing on the most vital functions.

### Regression Suite

The regression suite will provide comprehensive testing of the application, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

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
