# Test Plan: core_parabank

## Overview

This test plan outlines the testing strategy for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and identify potential issues introduced by recent changes.

## Scope

The testing scope encompasses account access, transfers & payments, and statements & history modules. The plan prioritizes critical paths and core business logic for smoke testing, while regression testing covers alternative flows, negative scenarios, and boundary conditions.

## Test Suites

### Smoke Suite

The smoke suite verifies the most critical functionalities of the application. It is designed to be executed quickly and efficiently to ensure the application's core features are working as expected.

#### Smoke Suite Strategy

The following checklist is applied to define the smoke suite for this project:

1.  **Critical Paths:** Focus on the most essential user flows (e.g., login, viewing account summary).
2.  **Core Business Logic:** Cover the primary revenue or operational flows.
3.  **Positive Testing:** Primarily focus on happy path scenarios.
4.  **No Negative Testing:** Exclude negative test cases unless they involve critical security concerns.
5.  **No Complex Edge Cases:** Avoid complex or less common scenarios.
6.  **Minimal Data Variation:** Use a limited set of test data.
7.  **Fast Execution:** Design tests for quick execution to enable rapid feedback.
8.  **Independence:** Ensure tests are independent and can be run in any order.

### Regression Suite

The regression suite provides comprehensive test coverage to ensure that new changes have not introduced defects into existing functionality. It includes a wide range of scenarios, including alternative flows, negative scenarios, and boundary conditions.

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
