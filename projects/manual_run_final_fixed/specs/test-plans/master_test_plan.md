# Test Plan: manual_run_final_fixed

## Introduction

This document outlines the test plan for the manual_run_final_fixed project, focusing on testing the login functionality of the Saucedemo website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover the login functionality of the Saucedemo website, including successful login scenarios.

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the login process. This includes ensuring that users can successfully log in with valid credentials.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** The login functionality is a critical path for accessing the application.
2.  **Core Business Logic:** Successful login is essential for using the application's features.
3.  **No Negative Testing:** The smoke suite will only focus on successful login with valid credentials.
4.  **No Complex Edge Cases:** The smoke suite will not cover edge cases or alternative login methods.
5.  **Fast Execution:** The smoke tests should be quick to execute to provide rapid feedback.
6.  **Independent Tests:** Each smoke test should be independent and not rely on the state of other tests.
7.  **High Priority:** Smoke tests are the highest priority and should be executed with every build.
8. **Automated:** Smoke tests should be automated to ensure consistent and reliable execution.

### Regression Suite

The regression suite will cover a broader range of scenarios, including alternative flows, negative scenarios, and boundary analysis. This will ensure that existing functionality remains intact after changes are made.

## Test Cases

Test cases will be developed for both the smoke and regression suites, covering various aspects of the login functionality.

## Test Environment

The tests will be executed in a standard web browser environment, such as Chrome or Firefox.

## Test Data

Test data will include valid and invalid credentials for testing the login functionality.

## Entry Criteria

-   The application is deployed to the test environment.
-   The test environment is stable and accessible.

## Exit Criteria

-   All test cases in the smoke suite have passed.
-   A sufficient number of test cases in the regression suite have passed, with any failures addressed and retested.

## Deliverables

-   Test plan document
-   Test cases
-   Test results
-   Defect reports
