# Test Plan: core_parabank

## Overview

This test plan outlines the testing strategy for the core_parabank application, focusing on verifying the login page, checking for the find transactions link (post-login), and navigating to the about us page. The plan includes both smoke and regression test suites to ensure comprehensive coverage.

## Scope

The scope of this test plan includes:

*   Verification of the login page elements.
*   Checking for the presence of the 'Find Transactions' link after successful login.
*   Navigation to the 'About Us' page.

## Test Suites

### Smoke Suite

The smoke suite will focus on the core functionality of the application, ensuring that the critical paths are working as expected. This suite will be executed after each build to quickly identify any major issues.

**Smoke Suite Strategy**

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

## Test Modules

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

## Environment

The tests will be executed in a dedicated test environment that closely mirrors the production environment.
