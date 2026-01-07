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

The following checklist has been applied when designing the Smoke Suite for this project:

1.  **Critical Paths Only**: Tests cover only the most essential workflows (e.g., login, basic transfer).  Complex scenarios are excluded.
2.  **Positive Testing**:  Focus is on successful execution of core functions.  Negative tests (e.g., invalid input) are skipped.
3.  **Minimal Data**:  Use a small, representative set of test data.
4.  **Independent Tests**:  Tests are designed to be independent and can be run in any order.
5.  **Fast Execution**:  Tests are optimized for speed to provide quick feedback.
6.  **Automated**:  All smoke tests are automated for consistent and repeatable execution.
7.  **Stable Locators**:  Use robust locators to minimize test failures due to UI changes.
8.  **Environment Stability**:  Smoke tests are run in a stable and dedicated environment.

### Regression Suite

The regression suite will provide comprehensive testing of the application, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

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
