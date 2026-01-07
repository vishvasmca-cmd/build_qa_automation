# Test Plan: core_parabank

## Overview

<<<<<<< Updated upstream
This test plan outlines the testing strategy for the core_parabank application, focusing on verifying the login page, checking for the find transactions link (post-login), and navigating to the about us page. The plan includes both smoke and regression test suites to ensure comprehensive coverage.
=======
This document outlines the test plan for the core_parabank application, focusing on verifying key functionalities within the banking domain. The plan includes both smoke and regression test suites to ensure application stability and quality.
>>>>>>> Stashed changes

## Scope

The scope of this test plan includes:

<<<<<<< Updated upstream
*   Verification of the login page elements.
*   Checking for the presence of the 'Find Transactions' link after successful login.
*   Navigation to the 'About Us' page.
=======
*   Account Access
*   Transfers & Payments
*   Statements & History
>>>>>>> Stashed changes

## Test Suites

### Smoke Suite

The smoke suite will focus on the core functionality of the application, ensuring that the critical paths are working as expected. This suite will be executed after each build to quickly identify any major issues.

**Smoke Suite Strategy**

<<<<<<< Updated upstream
The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover the most essential user flows (e.g., login).
2.  **Core Business Logic:** Focuses on primary functionalities related to banking operations.
3.  **Positive Testing:** Primarily uses valid inputs and expected outcomes.
4.  **No Negative Testing:** Excludes tests with invalid inputs or error conditions.
5.  **No Complex Edge Cases:** Avoids intricate scenarios or boundary conditions.
6.  **Speed of Execution:** Tests are designed to run quickly for rapid feedback.
7.  **Independence:** Tests are independent and do not rely on each other.
8.  **Minimal Data Setup:** Requires minimal or no pre-test data configuration.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, and boundary analysis. This suite will be executed periodically to ensure that new changes have not introduced any regressions.
=======
The following checklist is applied when designing the Smoke Suite for this project:

1.  **Critical Paths**: Tests cover the most important user workflows (e.g., login, basic transactions).  *CHECK*
2.  **Core Business Logic**: Focus on primary revenue or operational flows. *CHECK*
3.  **Positive Testing**: Primarily uses valid inputs and expected outcomes. *CHECK*
4.  **No Negative Testing**:  Skips invalid inputs or error conditions (unless critical security). *CHECK*
5.  **Minimal Edge Cases**: Avoids complex or unusual scenarios. *CHECK*
6.  **Fast Execution**:  Designed for quick turnaround to provide rapid feedback. *CHECK*
7.  **Build Validation**:  A failed smoke test indicates a critical issue, potentially rejecting the build. *CHECK*
8.  **Limited Scope**:  Focuses on breadth (covering multiple areas) rather than depth (detailed testing of one area). *CHECK*

#### Test Cases

*   Verify successful navigation to the About Us page.
*   Verify navigation to Account History page.

### Regression Suite

The regression suite will provide comprehensive testing of the application, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. This suite will be executed periodically to ensure that new changes have not introduced any regressions.
>>>>>>> Stashed changes

#### Test Cases

<<<<<<< Updated upstream
### Account Access (Criticality: Critical)

*   **Smoke Tests:**
    *   Verify Customer Login
*   **Regression Tests:**
    *   Login with invalid credentials
    *   Recover Forgotten Username/Password

### Statements & History (Criticality: Medium)

*   **Regression Tests:**
    *   Search Transactions by Keyword
    *   Filter Transactions by Amount Range

## Test Data

Test data will be used to simulate different user scenarios and ensure that the application behaves as expected under various conditions.
=======
*   Account Access:
    *   Login with invalid credentials.
    *   Recover forgotten password.
*   Transfers & Payments:
    *   Attempt to transfer exceeding balance.
    *   Schedule a future date transfer.
*   Statements & History:
    *   Download statement in PDF format.
    *   Search transactions by keyword.

## Test Environment

The tests will be executed in a stable test environment that mirrors the production environment.

## Test Data

Appropriate test data will be used to cover various scenarios and edge cases.
>>>>>>> Stashed changes

## Environment

<<<<<<< Updated upstream
The tests will be executed in a dedicated test environment that closely mirrors the production environment.
=======
*   Build deployed to the test environment.
*   Test environment is stable and accessible.
*   Test data is available and valid.

## Exit Criteria

*   All test cases in the smoke suite have passed.
*   Acceptable percentage of test cases in the regression suite have passed.
*   All critical and high severity defects have been resolved.
>>>>>>> Stashed changes
