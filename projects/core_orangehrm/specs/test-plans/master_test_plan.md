# Test Plan: core_orangehrm

## Introduction

This document outlines the test plan for the core_orangehrm project, focusing on verifying key functionalities of the OrangeHRM application. The tests will cover critical aspects of the login page, including elements, the 'Forgot Your Password?' link, and social media icons.

## Scope

The scope of this test plan includes:

*   Verification of login page elements (username, password fields, login button).
*   Functionality of the 'Forgot Your Password?' link.
*   Visibility and accessibility of social media icons on the login page.

## Test Strategy

The testing will be divided into Smoke and Regression test suites.

*   **Smoke Suite:** A high-level suite to ensure the core functionalities are working as expected.
*   **Regression Suite:** A more comprehensive suite to cover edge cases and ensure no regressions are introduced with new changes.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following checklist:

1.  **Critical Path Focus:** Tests will concentrate on the most critical paths (e.g., login).
2.  **Core Business Logic:** Verify the primary business logic related to authentication.
3.  **Positive Testing:** Primarily focus on positive test scenarios.
4.  **Minimal Data Variation:** Use a limited set of test data for speed and efficiency.
5.  **Independent Tests:** Each test should be independent and not rely on the state of others.
6.  **Fast Execution:** Tests should be designed for quick execution to provide rapid feedback.
7.  **Build Acceptance:** Successful completion of the Smoke Suite is a prerequisite for build acceptance.
8.  **Automated Execution:** The Smoke Suite will be automated for continuous integration.

## Test Suites

### Smoke Suite

The Smoke Suite will include the following test cases:

*   Verify the presence of login page elements (username, password fields, login button).
*   Verify the functionality of the 'Forgot Your Password?' link.
*   Verify the visibility of social media icons on the login page.

### Regression Suite

The Regression Suite will include the following test cases:

*   All Smoke test cases.
*   Negative login scenarios (invalid username/password).
*   Boundary testing for username and password fields.
*   Cross-browser compatibility testing.
*   Accessibility testing.

## Test Environment

The tests will be executed in the following environment:

*   Browser: Chrome, Firefox, Safari
*   Operating System: Windows, macOS, Linux
*   Test Framework: Playwright

## Test Deliverables

The following deliverables will be produced as part of the testing process:

*   Test Plan document
*   Test Cases
*   Test Scripts
*   Test Results
*   Defect Reports

