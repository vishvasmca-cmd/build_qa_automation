# Test Plan: core_orangehrm

## Introduction

This document outlines the test plan for the core_orangehrm project, focusing on verifying key functionalities of the OrangeHRM application. The application is a SaaS platform, and the tests will cover critical aspects like login page elements, password reset, and social media links.

## Scope

The testing will cover the following areas:

*   Verification of login page elements.
*   Functionality of the 'Forgot Password' link.
*   Visibility of social media icons.

## Test Strategy

We will employ both Smoke and Regression testing strategies to ensure comprehensive coverage.

*   **Smoke Testing:**  A quick, high-level test suite to verify the core functionalities are working after each build.
*   **Regression Testing:** A more in-depth test suite to ensure that new changes haven't introduced any regressions in existing functionalities.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following checklist:

1.  **Critical Paths Only:** Focus solely on the most essential workflows (e.g., login).
2.  **Positive Testing:** Primarily use valid inputs and expected outcomes.
3.  **Minimal Data Variation:** Use a small, representative set of test data.
4.  **No Edge Cases:** Avoid complex or unusual scenarios.
5.  **Fast Execution:** Tests should be quick to execute, providing rapid feedback.
6.  **Independent Tests:** Each test should be independent and not rely on the state of others.
7.  **Clear Pass/Fail Criteria:**  Define unambiguous criteria for test success or failure.
8.  **Automated Execution:**  Smoke tests should be automated for continuous integration.

## Test Suites

1.  **Smoke Suite:**
    *   Verify login page elements are present.
    *   Verify the 'Forgot Password' link is functional.
    *   Verify social media icons are visible on the login page.

2.  **Regression Suite:**
    *   (To be defined based on further analysis and feature development)

## Test Cases (Examples)

**Smoke Tests:**

*   **TC\_SMOKE\_001:** Verify Login Page Elements
    1.  Open the OrangeHRM login page.
    2.  Verify the presence of username field, password field, and login button.
*   **TC\_SMOKE\_002:** Verify 'Forgot Password' Link
    1.  Open the OrangeHRM login page.
    2.  Click on the 'Forgot your password?' link.
    3.  Verify that the user is redirected to the password reset page.
*   **TC\_SMOKE\_003:** Verify Social Media Icons
    1.  Open the OrangeHRM login page.
    2.  Scroll to the bottom of the page.
    3.  Verify that social media icons (e.g., LinkedIn, Facebook, Twitter) are visible.

## Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS
*   Test Framework: Playwright

## Test Data

*   Username: Admin
*   Password: (To be determined or reset)

## Entry Criteria

*   The application is deployed and accessible in the test environment.
*   Test environment is configured and ready.

## Exit Criteria

*   All planned tests have been executed.
*   All critical and high-priority defects have been resolved.
*   Test results have been documented and reviewed.
