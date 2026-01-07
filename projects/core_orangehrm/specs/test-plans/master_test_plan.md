# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, focusing on verifying key functionalities based on the provided user journey trace. The plan includes both smoke and regression test suites to ensure application stability and identify potential issues.

## Scope

The testing will cover the following areas:

*   Login page elements verification
*   'Forgot your password?' link functionality
*   Password reset process
*   Social media icons visibility on the login page

## Test Strategy

The testing strategy includes two main suites: Smoke and Regression.

*   **Smoke Suite:** A high-level suite to verify the core functionality.
*   **Regression Suite:** A more comprehensive suite to cover edge cases and ensure stability.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a quick assessment of the application's health. The following checklist is applied:

1.  **Critical Path Focus:** Tests cover the most critical user flows (e.g., login, password reset).
2.  **Positive Testing:** Primarily focuses on successful scenarios.
3.  **Minimal Data Variation:** Uses a limited set of test data.
4.  **Key Functionality:** Verifies core business logic is working.
5.  **Environment Stability:** Assumes a stable test environment.
6.  **Fast Execution:** Designed for quick execution and feedback.
7.  **Build Acceptance:** Used to determine if a build is acceptable for further testing.
8.  **Limited Scope:** Excludes complex edge cases and error handling.

## Test Suites

### Smoke Suite

The Smoke Suite will include the following test cases:

*   Verify the presence of login page elements (username, password, login button).
*   Verify the functionality of the 'Forgot your password?' link.
*   Verify the password reset process (filling username and clicking reset).
*   Verify navigation back to the login page from the password reset confirmation page.
*   Verify the presence of social media icons on the login page.

### Regression Suite

The Regression Suite will include the following test cases:

*   Invalid login attempts with different error messages.
*   Password reset with invalid username.
*   Verify error messages on the password reset page.
*   Verify social media icons link to the correct pages.
*   Test different browsers and devices.

## Test Environment

The tests will be executed on a stable test environment that mirrors the production environment.

## Test Deliverables

*   Test Plan document
*   Test Cases (Gherkin feature files)
*   Test Execution Reports

## Roles and Responsibilities

*   **QA Architect:** Responsible for creating and maintaining the test plan.
*   **QA Engineers:** Responsible for writing and executing test cases.

## входные и выходные данные

*   **Input:** User journey trace, domain information, project name.
*   **Output:** Test plan, Gherkin feature files, test execution reports.
