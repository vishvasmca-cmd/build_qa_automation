# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing will cover account access, transfers & payments, and statements & history functionalities. The focus will be on verifying critical paths and identifying potential issues through regression testing.

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. These tests are designed to be executed quickly and efficiently to ensure the application is in a stable state.

**Smoke Suite Strategy**

The following checklist was applied when designing the Smoke Suite:

1.  **Critical Paths**: Tests cover the most common and essential user flows.
2.  **Core Business Logic**: Focus on primary revenue or operational flows.
3.  **Positive Testing**: Primarily happy path scenarios.
4.  **No Negative Testing**: Unless critical security concerns exist.
5.  **No Complex Edge Cases**: Avoid intricate or rare scenarios.
6.  **Speed**: Tests should execute quickly.
7.  **Independence**: Tests should be independent of each other.
8.  **Minimal Data**: Use a small, consistent data set.

### Regression Suite

The regression suite will cover a broader range of functionalities, including alternative flows, negative scenarios, and boundary conditions. These tests are designed to ensure that new changes have not introduced any regressions in existing functionalities.

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
