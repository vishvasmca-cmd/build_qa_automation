# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities related to account access, transactions, and information retrieval. The plan includes both smoke and regression test suites to ensure application stability and reliability.

## Scope

The testing will cover the following modules:

*   Account Access
*   Transfers & Payments
*   Statements & History
*   About Us Page Navigation

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities of the application are working as expected. This suite will be executed for every build to quickly identify any major issues.

#### Smoke Suite Strategy

The following checklist was applied when designing the smoke suite for this project:

1.  **Critical Paths Only**: Focus solely on the most essential workflows (e.g., login).
2.  **Positive Testing**: Primarily use valid inputs and expected outcomes.
3.  **Minimal Data**: Use a small, representative set of test data.
4.  **No Edge Cases**: Avoid boundary conditions, error handling, or complex scenarios.
5.  **Fast Execution**: Design tests for quick completion and rapid feedback.
6.  **Independent Tests**: Ensure each test can run independently without dependencies.
7.  **High Priority**: Address any failures in the smoke suite immediately.
8.  **Automated Execution**: Automate the smoke suite for continuous integration.

### Regression Suite

The regression suite will provide comprehensive testing of the application, including alternative flows, negative scenarios, and boundary conditions. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

## Test Modules

### Account Access (Criticality: Critical)

*   **Smoke Tests:**
    *   Verify Customer Login
*   **Regression Tests:**
    *   Login with invalid credentials
    *   Recover Forgotten Username/Password
    *   Session Timeout Handling

### Statements & History (Criticality: Medium)

*   **Smoke Tests:**
    *   Verify navigation to Account History

### About Us (Criticality: Low)

*   **Smoke Tests:**
    *   Verify navigation to About Us page

## Test Environment

The tests will be executed in a staging environment that mirrors the production environment.

## Test Data

Test data will be created and managed to support the execution of both smoke and regression tests.

## Entry Criteria

*   The application build must be successfully deployed to the test environment.
*   All required test data must be available.

## Exit Criteria

*   All smoke tests must pass.
*   A defined percentage of regression tests must pass.
*   All critical and high-priority defects must be resolved.
