# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.

## Scope

The testing will cover account access, transfers & payments, and statements & history modules. The focus will be on critical user workflows and potential edge cases.

## Test Suites

### Smoke Suite

The smoke suite will verify the core functionalities of the application. These tests are designed to be executed quickly and should identify any major issues that would prevent further testing.

**Smoke Suite Strategy**

The following checklist was applied when designing the smoke suite for this project:

1.  **Critical Paths:** Tests cover the most common and essential user flows (e.g., login).
2.  **Core Business Logic:** Focus on verifying the primary functions related to the banking domain.
3.  **Positive Testing:** Primarily focuses on successful scenarios, with minimal negative testing.
4.  **End-to-End Coverage:** Tests simulate real user interactions from start to finish for key workflows.
5.  **Data Integrity:** Basic validation of data consistency throughout the tested flows.
6.  **Environment Stability:** Checks for basic environment issues that might block testing.
7.  **Performance Considerations:** No performance tests are included in the smoke suite.
8.  **Security Considerations:** Basic security checks (e.g., login) are included.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

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
