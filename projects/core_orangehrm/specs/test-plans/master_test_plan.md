# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, a SaaS platform. The plan includes smoke and regression testing strategies to ensure the quality and stability of the application.

## Scope

The testing will cover the following areas:

*   Login page elements verification
*   'Forgot your password?' link functionality
*   Social media icons visibility

## Testing Strategy

### Smoke Suite Strategy

The smoke suite will focus on verifying the core functionality of the application. The following checklist will be applied:

1.  **Critical Path Coverage:** Tests cover the most common and important user flows.
2.  **Positive Testing:** Focus on successful scenarios, not error handling.
3.  **End-to-End Flow:** Tests cover the entire flow from start to finish.
4.  **Data Integrity:** Verify that data is correctly created, read, updated, and deleted (CRUD).
5.  **Minimal Complexity:** Tests are simple and easy to understand.
6.  **Fast Execution:** Tests should run quickly to provide rapid feedback.
7.  **Environment Stability:** Tests assume a stable and properly configured environment.
8.  **Build Acceptance:** Passing smoke tests indicate a build is acceptable for further testing.

### Regression Suite Strategy

The regression suite will cover a broader range of scenarios, including edge cases and error handling. This suite will be executed after the smoke tests have passed.

## Test Suites

1.  Smoke Suite: Verifies the basic functionality of the login page, forgot password link, and social media icons.
2.  Regression Suite: Includes more detailed tests for the login page, forgot password functionality, and social media icons, including negative scenarios and edge cases.

## Test Cases

Detailed test cases will be created for each test suite, covering the specific scenarios to be tested.
