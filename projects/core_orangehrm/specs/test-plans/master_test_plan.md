# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, focusing on verifying key functionalities and ensuring application stability. The plan includes both smoke and regression test suites to provide comprehensive coverage.

## Scope

The scope of this test plan includes:

*   Verification of login page elements.
*   Functionality of the "Forgot your password?" link.
*   Navigation through the password reset process.
*   Verification of social media icons on the login page (if present).

## Test Strategy

This project will employ a two-tiered testing strategy:

1.  **Smoke Suite:** A quick, high-level suite to ensure the core functionalities are working as expected.
2.  **Regression Suite:** A more comprehensive suite to ensure that new changes haven't introduced any regressions.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a rapid assessment of the application's health. The following checklist is applied:

1.  **Critical Functionality:** Tests cover the most critical paths (e.g., login, password reset).
2.  **Positive Testing:** Focus is on positive scenarios (e.g., successful password reset request).
3.  **Minimal Data Variation:** Use a small, representative set of data.
4.  **Fast Execution:** Tests are designed to execute quickly.
5.  **Independent Tests:** Tests should be independent and not rely on each other.
6.  **Clear Pass/Fail Criteria:** Each test has a clear and unambiguous pass/fail criterion.
7.  **Automated Execution:** The suite is designed for automated execution.
8.  **Build Acceptance:** Successful completion of the Smoke Suite is a prerequisite for build acceptance.

## Test Suites

### 1. Smoke Suite

*   **Description:** This suite verifies the basic functionality of the login page and the password reset flow.
*   **Focus:**
    *   Verify the presence of login page elements.
    *   Verify the functionality of the "Forgot your password?" link.
    *   Verify that a password reset request can be submitted.
    *   Verify navigation back to the login page.*   **Test Cases:***   Verify login page elements are displayed.*   Verify "Forgot your password?" link navigates to the reset password page.*   Submit a password reset request with a valid username.*   Verify navigation back to the login page from the password reset confirmation page.

### 2. Regression Suite

*   **Description:** This suite provides a more in-depth analysis of the application, covering edge cases and negative scenarios.
*   **Focus:**
    *   Negative password reset scenarios (e.g., invalid username).
    *   Verification of error messages.
    *   Verification of social media icons (if present).
*   **Test Cases:***   Attempt to reset password with an invalid username.*   Verify error message for invalid username.*   Verify social media icons are displayed and functional (if present).

## Test Deliverables

*   Test Plan document
*   Test Cases (Gherkin Feature Files)
*   Test Execution Reports

