# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities related to the login page, finding transactions, and navigating to the 'About Us' page. The test plan includes both smoke and regression test suites to ensure comprehensive coverage.

## Scope

The scope of this test plan includes:

*   Verification of the login page elements.
*   Checking the availability of the 'Find Transactions' functionality (or a similar feature).
*   Navigation to the 'About Us' page.

## Test Suites

### Smoke Suite

The smoke suite will focus on the core functionalities to ensure the application's basic health.  It will cover the happy path scenarios.

#### Smoke Suite Strategy

The following 8-point checklist is applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Include tests for the most critical user flows (e.g., login).
2.  **Core Business Logic:** Verify the primary business functions are working.
3.  **Positive Testing:** Focus on valid inputs and expected outcomes.
4.  **No Negative Testing:** Exclude tests with invalid inputs or error conditions.
5.  **Minimal Data Set:** Use a small, representative set of test data.
6.  **Fast Execution:** Design tests for quick execution to provide rapid feedback.
7.  **Independent Tests:** Ensure tests are independent and can be run in any order.
8.  **High Priority Defects:** Cover scenarios related to recently fixed high-priority defects.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including edge cases, alternative flows, and negative scenarios. This suite will ensure that new changes haven't introduced regressions in existing functionalities.

## Test Modules

### Account Access (Criticality: Critical)

*   **Smoke Tests:**
    *   Verify the login page is displayed correctly.
    *   Verify navigation to the 'About Us' page.
*   **Regression Tests:**
    *   (Not covered by the trace, but would be included in a full regression suite) Test login with valid and invalid credentials.
    *   (Not covered by the trace, but would be included in a full regression suite) Test password recovery.

### Transfers & Payments (Criticality: Critical)

*   **Smoke Tests:**
    *   (Not covered by the trace, but would be included in a full regression suite) Verify the availability of the 'Find Transactions' link/functionality after login.
*   **Regression Tests:**
    *   (Not covered by the trace, but would be included in a full regression suite) Test searching transactions by different criteria (date, amount, etc.).
    *   (Not covered by the trace, but would be included in a full regression suite) Test the display of transaction details.

## Test Data

*   For the smoke tests, minimal test data will be used.
*   For the regression tests, a more comprehensive set of test data will be used to cover various scenarios.

## Test Environment

*   The tests will be executed in a stable test environment that mirrors the production environment.

## Entry Criteria

*   The application build must be successfully deployed to the test environment.
*   All necessary test data must be available.

## Exit Criteria

*   All smoke tests must pass for the build to be considered stable.
*   A defined percentage of regression tests must pass before release.

## Test Deliverables

*   Test Plan document
*   Test Cases (Gherkin feature files)
*   Test Execution Reports

