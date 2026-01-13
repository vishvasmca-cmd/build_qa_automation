# Test Plan: OrangeHRM Employee Management

## Introduction

This test plan outlines the testing strategy for the OrangeHRM employee management functionality, focusing on adding a new employee. The plan includes smoke and regression test suites to ensure the application's stability and functionality.

## Scope

The scope of this test plan covers the following functionality:

*   Login to OrangeHRM
*   Navigating to the PIM (Personnel Information Management) module.
*   Adding a new employee with first name and last name.
*   Verifying the successful creation of the employee and navigation to the employee's personal details page.

## Test Strategy

The testing strategy consists of two main suites: Smoke and Regression.

*   **Smoke Suite:**  A quick set of tests to verify the core functionality is working after a build or deployment.
*   **Regression Suite:** A more comprehensive set of tests to ensure that new changes haven't introduced any regressions in existing functionality.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a rapid assessment of the application's health. The following checklist is applied:

1.  **Critical Path Coverage:**  Covers the most essential user flow (login, add employee).
2.  **Positive Testing:** Focuses on successful scenarios (e.g., valid credentials, valid data).
3.  **Minimal Data Variation:** Uses a single set of test data for simplicity.
4.  **No Error Handling:**  Does not explicitly test error conditions.
5.  **Fast Execution:**  Designed to run quickly to provide immediate feedback.
6.  **Build Acceptance:**  Passing smoke tests are a prerequisite for build acceptance.
7.  **Automated Execution:**  Smoke tests are automated for continuous integration.
8.  **Limited Scope:**  Focuses solely on core functionality, excluding edge cases.

## Test Suites

### 1. Smoke Suite

*   **Description:**  Verifies the basic functionality of logging in and adding a new employee.
*   **Focus:**  Critical path, positive testing.
*   **Test Cases:**
    *   Successful login with valid credentials.
    *   Adding a new employee with valid first name and last name.
    *   Verifying navigation to the employee's personal details page after creation.

### 2. Regression Suite

*   **Description:**  Ensures that new changes haven't broken existing functionality related to employee management.
*   **Focus:**  Alternative flows, negative scenarios, boundary analysis, cross-module interactions, and validation messages.
*   **Test Cases:**
    *   Invalid login attempts with incorrect credentials.
    *   Attempting to add an employee with missing first name.
    *   Attempting to add an employee with missing last name.
    *   Verifying error messages for invalid input.
    *   Checking data persistence after adding an employee.
    *   Verifying the display of the new employee in the employee list.

## Test Data

*   Valid Username: Admin
*   Valid Password: admin123
*   First Name: Resilience
*   Last Name: Agent

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   Environment:  https://opensource-demo.orangehrmlive.com/

## Entry Criteria

*   The application build is deployed to the test environment.
*   Test data is prepared.

## Exit Criteria

*   All planned test cases have been executed.
*   All critical and high-priority defects have been resolved.
*   Test results are documented.
