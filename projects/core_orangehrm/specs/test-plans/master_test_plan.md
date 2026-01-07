# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm project, focusing on verifying key functionalities related to the login page and password reset flow. The application under test is a SaaS platform.

## Scope

The scope of this test plan includes:

*   Verification of login page elements.
*   Functionality of the "Forgot your password?" link.
*   Password reset process.
*   Navigation between pages.
*   Verification of social media icons on the login page.

## Test Strategy

The testing will be conducted using a combination of smoke and regression testing.

### Smoke Suite Strategy

The smoke suite will focus on the critical path of the application. The following checklist is applied to define the smoke suite:

1.  **Critical Paths:** Tests cover essential functionalities like accessing the login page and initiating the password reset process.
2.  **Core Business Logic:** Focuses on the primary function of user authentication and password recovery.
3.  **Positive Testing:** Primarily focuses on successful scenarios (e.g., clicking the "Forgot your password?" link).
4.  **No Negative Testing:** Negative scenarios like invalid username are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios or boundary conditions are not included.
6.  **Fast Execution:** The smoke suite is designed to be executed quickly to provide rapid feedback.
7.  **Build Acceptance:** Successful completion of the smoke suite is a prerequisite for build acceptance.
8.  **Limited Scope:** The suite covers a minimal set of functionalities to ensure the system's basic health.

### Regression Suite Strategy

The regression suite will provide a comprehensive test coverage to ensure that new changes have not introduced any regressions. This will include:

*   Alternative flows.
*   Negative scenarios.
*   Boundary analysis.
*   Cross-module interactions.
*   Validation messages.

## Test Suites

1.  **Smoke Suite:**
    *   Verify the presence of login page elements.
    *   Verify the functionality of the "Forgot your password?" link.
    *   Initiate the password reset process.
    *   Verify navigation back to the login page.
    *   Verify the presence of social media icons on the login page.

2.  **Regression Suite:** (To be defined in detail later)
    *   Test with invalid username and password.
    *   Test password reset with different username formats.
    *   Verify error messages.
    *   Test social media links.

## Test Environment

The tests will be executed on the following environment:

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/11, macOS

## Test Deliverables

*   Test Plan
*   Test Cases (Gherkin Feature Files)
*   Test Execution Reports

## Test Automation

*   The tests will be automated using Playwright.
*   Gherkin syntax will be used to define the test cases.

