# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, a SaaS platform. The plan includes smoke and regression test suites designed to ensure the quality and stability of the application.

## Scope

The testing will cover the following areas:

*   Login functionality
*   Password reset functionality
*   Verification of social media icons on the login page

## Test Suites

### Smoke Suite

The smoke suite will focus on the critical path of the application. It will verify the core functionality is working as expected.

#### Smoke Suite Strategy

The Smoke Suite for this project adheres to the following 8-point checklist:

1.  **Critical Paths Only:** Focuses solely on the most essential workflows (Login, Password Reset).
2.  **Positive Testing:** Primarily uses valid inputs and expected actions.
3.  **No Edge Cases:** Avoids complex scenarios or boundary conditions.
4.  **Fast Execution:** Designed for quick feedback on build stability.
5.  **Independent Tests:** Each test can be run in isolation.
6.  **Clear Pass/Fail Criteria:** Easy to determine the outcome of each test.
7.  **Automated Execution:** Fully automated for continuous integration.
8.  **Build Validation:** Used to determine if a build is acceptable for further testing.

#### Smoke Test Cases

*   Verify login page elements are displayed.
*   Verify the 'Forgot your password?' link navigates to the password reset page.
*   Verify the password reset functionality.
*   Verify social media icons are displayed on the login page.

### Regression Suite

The regression suite will cover a broader range of functionality, including alternative flows, negative scenarios, and boundary conditions. This suite ensures that new changes have not introduced defects into existing functionality.

#### Regression Test Cases

*   Verify login with valid and invalid credentials.
*   Verify password reset with valid and invalid usernames.
*   Verify error messages are displayed for invalid login attempts.
*   Verify the functionality of all links on the login page.
*   Verify the display and functionality of social media icons on the login page.

## Test Environment

The tests will be executed in the following environment:

*   Browser: Chrome
*   Operating System: Windows 10
*   Test Framework: Playwright

## Test Data

Test data will be used to simulate various scenarios and ensure the application handles different types of input correctly. This includes valid and invalid usernames and passwords.

## Test Execution

The tests will be executed automatically as part of the continuous integration process. Results will be reported to a central dashboard for analysis.
