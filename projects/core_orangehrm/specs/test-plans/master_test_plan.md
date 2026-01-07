# Test Plan: core_orangehrm

## Introduction

This document outlines the test plan for the core_orangehrm project, focusing on verifying key functionalities of the OrangeHRM application. The tests will cover login page elements, the 'Forgot Password' flow, and the visibility of social media icons.

## Scope

The scope of this test plan includes:

*   Verification of login page elements.
*   Testing the 'Forgot your password?' link functionality.
*   Checking the password reset process.
*   Verification of social media icons on the login page.

## Test Strategy

This test plan employs a two-tiered testing strategy:

1.  **Smoke Testing:** A high-level suite to ensure the core functionalities are working as expected.
2.  **Regression Testing:** A more comprehensive suite to cover various scenarios and edge cases.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following checklist:

1.  **Critical Path Focus:** Tests will concentrate on the most critical paths (e.g., login, password reset).
2.  **Core Business Logic:** Verification of the primary business logic related to authentication.
3.  **Positive Testing:** Primarily positive testing, ensuring successful execution of core functionalities.
4.  **No Negative Testing:** Negative scenarios (e.g., invalid login attempts) are excluded from the smoke suite.
5.  **Minimal Edge Cases:** Complex edge cases are not considered in the smoke suite.
6.  **Fast Execution:** Tests are designed for quick execution to provide rapid feedback.
7.  **Build Acceptance:** Failure of any smoke test indicates a critical issue, potentially rejecting the build.
8.  **Happy Path**: Tests follow the most common and straightforward user flows.

## Test Suites

### 1. Smoke Suite

*   **Description:** A set of critical tests to verify the basic functionality of the application.
*   **Focus:** Login page elements, 'Forgot Password' flow.
*   **Environment:** Staging

### 2. Regression Suite

*   **Description:** A comprehensive set of tests to ensure that new changes have not introduced regressions.
*   **Focus:** All functionalities, including edge cases and negative scenarios.
*   **Environment:** Staging

## Test Cases (Examples)

**Smoke Suite:**

*   Verify that all login page elements are displayed correctly.
*   Verify that the 'Forgot your password?' link redirects to the password reset page.
*   Verify that a user can request a password reset.
*   Verify that social media icons are displayed on the login page.

**Regression Suite:**

*   Verify that a user can log in with valid credentials.
*   Verify that a user cannot log in with invalid credentials.
*   Verify that the password reset functionality works correctly with a valid username.
*   Verify that the password reset functionality displays an error message with an invalid username.
*   Verify the appearance and functionality of all elements on the login page across different browsers and devices.

## Test Environment

*   **Browser:** Chrome, Firefox, Safari, Edge
*   **Operating System:** Windows, macOS, Linux
*   **Environment:** Staging

## Test Deliverables

*   Test Plan document
*   Test Cases
*   Test Scripts
*   Test Results
*   Defect Reports
