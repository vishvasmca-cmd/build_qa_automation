# Test Plan: core_orangehrm

## Introduction

This document outlines the test plan for the core_orangehrm project, focusing on verifying login page elements, checking the 'Forgot your password?' link functionality, and ensuring social media icons are visible on the login page.

## Scope

The testing will cover the following areas:

*   Login page elements verification (username, password fields, login button).
*   'Forgot your password?' link functionality (navigation and form submission).
*   Social media icons visibility on the login page.

## Test Strategy

The testing will be conducted using a combination of smoke and regression testing techniques.

### Smoke Suite Strategy

The smoke suite will focus on the critical path of the login process and the 'Forgot your password?' functionality. The following 8-point checklist has been applied to define the smoke suite:

1.  **Critical Paths:** Focuses on the primary login flow and password reset initiation.
2.  **Core Business Logic:** Verifies the core functionality of user authentication.
3.  **No Negative Testing:** No invalid login attempts or error conditions are tested in the smoke suite.
4.  **No Complex Edge Cases:** No boundary conditions or unusual scenarios are included.
5.  **Positive Testing Only:** Only successful password reset initiation is tested.
6.  **Essential Functionality:** Only the basic 'Forgot Password' flow is covered.
7.  **High-Level Scenarios:** Only the initial steps of the flow are tested.
8.  **Limited Data Variation:** Only a single user is used (if login was involved).

### Regression Suite Strategy

The regression suite will cover a broader range of scenarios, including:

*   Invalid login attempts with different error messages.
*   Password reset with invalid username.
*   Verification of error messages and validation rules.
*   Checking the visibility and functionality of all social media icons.
*   Testing with different browsers and devices.

## Test Environment

The tests will be executed on the following environment:

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   Test Framework: Playwright

## Test Deliverables

The following deliverables will be produced as part of the testing process:

*   Test Plan
*   Test Cases (Gherkin Feature Files)
*   Test Execution Reports
*   Defect Reports

## Test Schedule

The testing will be conducted according to the following schedule:

*   Test Planning: \[Start Date] - \[End Date]
*   Test Case Development: \[Start Date] - \[End Date]
*   Test Execution: \[Start Date] - \[End Date]
*   Defect Reporting: Ongoing
*   Regression Testing: \[Start Date] - \[End Date]

## Entry Criteria

*   The application is deployed to the test environment.
*   The test environment is properly configured.
*   Test data is available.

## Exit Criteria

*   All test cases have been executed.
*   All identified defects have been resolved and retested.
*   The application meets the defined quality standards.

## Risks and Mitigation

*   Risk: Test environment instability.
*   Mitigation: Ensure a stable test environment is available.
*   Risk: Lack of test data.
*   Mitigation: Prepare test data in advance.
