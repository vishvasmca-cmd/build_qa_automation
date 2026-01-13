# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be automated and integrated into a Continuous Integration (CI) pipeline to ensure the quality and stability of the application.

## Scope

The scope of this test plan includes:

*   Smoke tests to verify core functionality.
*   Regression tests to ensure existing functionality remains intact after changes.

## Test Strategy

We will employ a two-pronged testing strategy:

1.  **Smoke Testing:** A quick and efficient way to validate the most critical functionalities of the application.
2.  **Regression Testing:** A more comprehensive approach to ensure that new changes do not negatively impact existing features.

### Smoke Suite Strategy

The following checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Focus on the most essential user journeys (e.g., search, add to cart, checkout).
2.  **Core Business Logic:** Verify the fundamental business rules are functioning correctly.
3.  **Positive Testing:** Primarily focus on successful scenarios.
4.  **Minimal Data Variation:** Use a limited set of representative data.
5.  **Fast Execution:** Design tests for quick execution to provide rapid feedback.
6.  **Independent Tests:** Ensure tests can be run independently without dependencies.
7.  **High Priority:** Address any failures immediately.
8.  **Automated Execution:** Automate the smoke tests for continuous integration.

## Test Suites

1.  **Smoke Suite:**
    *   Purpose: To ensure the core functionality of the application is working as expected.
    *   Frequency: Run on every build.
    *   Environment: Staging environment.
    *   Data: Representative data set.

2.  **Regression Suite:**
    *   Purpose: To ensure that new changes do not break existing functionality.
    *   Frequency: Run nightly or on demand.
    *   Environment: Staging environment.
    *   Data: Comprehensive data set, including edge cases and negative scenarios.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Framework: Playwright
*   CI/CD: GitHub Actions

## Test Data

Test data will be managed within the test framework and will include:

*   Valid search terms (e.g., Dyson V15 Detect).
*   Valid user credentials (for future login scenarios).

## Test Deliverables

*   Automated test scripts (Playwright).
*   Test execution reports.
*   Defect tracking in Jira (if applicable).

## Roles and Responsibilities

*   QA Architect: Responsible for defining the test strategy and test plan.
*   QA Engineers: Responsible for writing and executing automated tests.
*   Developers: Responsible for fixing defects.

## Entry Criteria

*   Build deployed to the staging environment.
*   Test environment configured.
*   Test data available.

## Exit Criteria

*   All smoke tests pass.
*   Regression tests pass with an acceptable defect rate.
*   Test execution reports generated.
