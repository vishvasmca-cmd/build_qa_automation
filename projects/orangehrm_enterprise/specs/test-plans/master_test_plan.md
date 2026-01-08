# Test Plan: OrangeHRM Enterprise

## Introduction

This test plan outlines the testing strategy for the OrangeHRM Enterprise application. The plan includes smoke and regression test suites designed to ensure the quality and stability of the application.

## Scope

The scope of testing includes:

*   Login functionality
*   PIM (Personnel Information Management) module
*   Adding new employees
*   Admin module
*   User Management
*   Creating system users

## Test Suites

### Smoke Suite

The smoke suite verifies the core functionality of the application. It focuses on critical paths and ensures that the system is stable enough for further testing.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths Only:** Focuses solely on essential workflows (Login, Add Employee, Create User).
2.  **Positive Testing:** Uses valid data and expected actions to confirm core functionality.
3.  **No Edge Cases:** Excludes boundary conditions, error handling, or alternative flows.
4.  **Fast Execution:** Designed for quick execution to provide rapid feedback on build stability.
5.  **Independent Tests:** Each test can be run independently without dependencies on other tests.
6.  **High Priority:** Any failure in the smoke suite indicates a critical issue and blocks further testing.
7.  **Limited Data Variation:** Uses a minimal set of data to cover the primary scenarios.
8.  **Automated Execution:** The smoke suite is designed for automated execution as part of the CI/CD pipeline.

### Regression Suite

The regression suite ensures that new changes have not introduced defects into existing functionality. It includes a broader range of tests, covering alternative flows, negative scenarios, and boundary conditions.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files.

## Test Environment

The tests will be executed against the following environment:

*   URL: https://opensource-demo.orangehrmlive.com/
*   Browser: Chrome (latest version)
*   Operating System: Windows 10

## Test Data

Test data will be created and managed to support the test cases. This includes user credentials, employee information, and other relevant data.

## Entry Criteria

*   The application build must be successfully deployed to the test environment.
*   All necessary test data must be available.

## Exit Criteria

*   All test cases in the smoke suite must pass.
*   A defined percentage of test cases in the regression suite must pass (e.g., 95%).
*   All critical and high-priority defects must be resolved.

## Roles and Responsibilities

*   QA Architect: Responsible for creating and maintaining the test plan.
*   QA Engineers: Responsible for writing and executing test cases.
*   Developers: Responsible for fixing defects.

## Tools

*   Playwright: Test automation framework
*   GitHub: Version control
*   TestRail: Test case management
