# Test Plan: core_parabank

## Overview

This test plan outlines the testing strategy for the core_parabank application, focusing on key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing will cover account access, transfers & payments, and statements & history functionalities.

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities of the application are working as expected.  It will provide a quick assessment of the application's health after deployment or code changes.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover the most essential user workflows (e.g., login).
2.  **Core Business Logic:** Focus on primary revenue or operational flows.
3.  **Positive Testing:** Primarily focuses on successful scenarios.
4.  **No Negative Testing:** Excludes negative test cases unless critical for security.
5.  **No Complex Edge Cases:** Avoids intricate or unusual scenarios.
6.  **Fast Execution:** Designed for quick execution to provide rapid feedback.
7.  **Independent Tests:** Tests should be independent and not rely on each other.
8.  **Limited Data Dependency:** Minimize reliance on specific test data.

### Regression Suite

The regression suite will provide a comprehensive test coverage to ensure that new changes have not introduced defects into existing functionalities. It will include alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

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
