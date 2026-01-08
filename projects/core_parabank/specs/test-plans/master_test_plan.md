# Test Plan: core_parabank

## Overview

This test plan outlines the testing strategy for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing scope covers account access, transfers & payments, and statements & history modules. The initial focus is on smoke testing to validate critical paths, followed by regression testing to cover variations, edge cases, and error handling.

## Test Suites

### Smoke Suite

The smoke suite is designed to quickly verify the core functionalities of the application. It includes tests for:

*   Customer Login
*   View Account Dashboard

#### Smoke Suite Strategy

The following checklist was applied when designing the smoke suite for this project:

1.  **Critical Paths:** Tests cover the most essential user flows (e.g., login).
2.  **Core Business Logic:** Focus on primary revenue/operation flows.
3.  **Positive Testing:** Primarily happy path scenarios.
4.  **No Negative Testing:** Unless critical security is involved.
5.  **No Complex Edge Cases:** Avoid intricate scenarios in smoke tests.
6.  **Fast Execution:** Tests should be quick to execute for rapid feedback.
7.  **Independent Tests:** Tests should be independent and not rely on each other.
8.  **High Priority:** Any failures in the smoke suite should be treated as critical.

### Regression Suite

The regression suite provides comprehensive test coverage, including:

*   Alternative Flows
*   Negative Scenarios
*   Boundary Analysis
*   Cross-Module Interactions
*   Validation Messages

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
