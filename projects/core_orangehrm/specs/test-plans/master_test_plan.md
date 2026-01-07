# Test Plan: core_orangehrm

## Introduction

<<<<<<< Updated upstream
This test plan outlines the testing strategy for the core_orangehrm application, focusing on verifying key functionalities based on the provided user journey trace. The plan includes both smoke and regression test suites to ensure application stability and identify potential issues.
=======
This test plan outlines the testing strategy for the core_orangehrm application, focusing on verifying key functionalities related to login, password reset, and social media presence. The plan includes both smoke and regression test suites to ensure comprehensive coverage.
>>>>>>> Stashed changes

## Scope

This test plan covers the following areas:

*   Login page elements verification
*   'Forgot your password?' link functionality
*   Password reset process
*   Social media icons visibility on the login page

## Test Strategy

<<<<<<< Updated upstream
The testing strategy includes two main suites: Smoke and Regression.

*   **Smoke Suite:** A high-level suite to verify the core functionality.
*   **Regression Suite:** A more comprehensive suite to cover edge cases and ensure stability.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a quick assessment of the application's health. The following checklist is applied:

1.  **Critical Path Focus:** Tests cover the most critical user flows (e.g., login, password reset).
2.  **Positive Testing:** Primarily focuses on successful scenarios.
3.  **Minimal Data Variation:** Uses a limited set of test data.
4.  **Key Functionality:** Verifies core business logic is working.
5.  **Environment Stability:** Assumes a stable test environment.
6.  **Fast Execution:** Designed for quick execution and feedback.
7.  **Build Acceptance:** Used to determine if a build is acceptable for further testing.
8.  **Limited Scope:** Excludes complex edge cases and error handling.
=======
The testing strategy includes two main suites:

1.  **Smoke Suite:** A high-level suite to verify the core functionality of the application.
2.  **Regression Suite:** A comprehensive suite to ensure that new changes do not negatively impact existing functionality.

### Smoke Suite Strategy

The Smoke Suite is designed to provide a quick and efficient way to verify the stability of the application. The following checklist is applied:

1.  **Critical Path Focus:** Tests cover the most critical user flows (e.g., login, password reset).
2.  **Positive Testing:** Primarily focuses on positive scenarios (happy path).
3.  **Minimal Data Variation:** Uses a limited set of test data.
4.  **Key Functionality:** Verifies core business logic.
5.  **Environment Stability:** Ensures the test environment is stable before execution.
6.  **Fast Execution:** Tests are designed to execute quickly.
7.  **Build Acceptance:** Successful completion indicates a stable build.
8.  **Automated Execution:** Tests are automated for rapid feedback.
>>>>>>> Stashed changes

## Test Suites

### Smoke Suite

<<<<<<< Updated upstream
The Smoke Suite will include the following test cases:

*   Verify the presence of login page elements (username, password, login button).
*   Verify the functionality of the 'Forgot your password?' link.
*   Verify the password reset process (filling username and clicking reset).
*   Verify navigation back to the login page from the password reset confirmation page.
=======
*   Verify the presence of login page elements (username, password, login button).
*   Verify the functionality of the 'Forgot your password?' link.
*   Verify the password reset process.
>>>>>>> Stashed changes
*   Verify the presence of social media icons on the login page.

### Regression Suite

<<<<<<< Updated upstream
The Regression Suite will include the following test cases:

*   Invalid login attempts with different error messages.
*   Password reset with invalid username.
*   Verify error messages on the password reset page.
*   Verify social media icons link to the correct pages.
*   Test different browsers and devices.

## Test Environment

The tests will be executed on a stable test environment that mirrors the production environment.

## Test Deliverables

*   Test Plan document
*   Test Cases (Gherkin feature files)
*   Test Execution Reports

## Roles and Responsibilities

*   **QA Architect:** Responsible for creating and maintaining the test plan.
*   **QA Engineers:** Responsible for writing and executing test cases.

## входные и выходные данные

*   **Input:** User journey trace, domain information, project name.
*   **Output:** Test plan, Gherkin feature files, test execution reports.
=======
*   **Login Functionality:**
    *   Valid login with correct credentials.
    *   Invalid login with incorrect credentials.
    *   Login with empty username and password.
    *   Login with special characters in username and password.
*   **Forgot Password Functionality:**
    *   Request password reset with a valid username.
    *   Request password reset with an invalid username.
    *   Verify the password reset email is sent.
    *   Reset password with a valid token.
    *   Reset password with an invalid token.
*   **Social Media Icons:**
    *   Verify the presence of all social media icons.
    *   Verify the links to social media pages are correct.
    *   Verify the icons are displayed correctly on different browsers and devices.

## Test Cases

Test cases will be documented in detail within the test management system, linking back to these features.
>>>>>>> Stashed changes
