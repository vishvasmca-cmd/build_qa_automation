# Test Plan for core_orangehrm

## Introduction

This document outlines the test plan for the core_orangehrm project, focusing on verifying key functionalities of the OrangeHRM application. The tests will cover critical aspects of the login page, password reset process, and social media links.

## Scope

The testing will cover the following areas:

*   Login page elements verification
*   'Forgot your password?' link functionality
*   Password reset process
*   Social media icons visibility

## Test Strategy

We will employ a two-pronged testing strategy:

1.  **Smoke Testing:** A quick and shallow test to ensure the core functionalities are working as expected.
2.  **Regression Testing:** A more comprehensive test suite to ensure that new changes haven't introduced any regressions.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following checklist:

1.  **Critical Path Focus:** Tests will focus on the most critical paths (e.g., login, password reset).
2.  **Core Business Logic:** Verify the primary business logic related to authentication.
3.  **Positive Testing:** Primarily focus on positive test cases (happy path).
4.  **No Negative Testing:** Exclude negative testing unless it relates to critical security aspects.
5.  **No Complex Edge Cases:** Avoid complex or less common scenarios.
6.  **Fast Execution:** Tests should be quick to execute to provide rapid feedback.
7.  **Build Validation:** Smoke tests will be executed after each build to validate its stability.
8.  **Automated Execution:** Smoke tests will be automated for continuous integration.

## Test Suites

### 1. Smoke Suite

*   Verify login page elements are displayed.
*   Verify the 'Forgot your password?' link is present and navigates to the password reset page.
*   Verify the password reset functionality by entering a username and submitting the reset request.
*   Verify navigation back to the login page from the password reset confirmation page.
*   Verify social media icons are displayed on the login page.

### 2. Regression Suite

*   **Login Functionality:**
    *   Valid login with correct credentials.
    *   Invalid login with incorrect credentials.
    *   Login with empty username and password.
    *   Login with special characters in username and password.
*   **Forgot Password Functionality:**
    *   Reset password with a valid username.
    *   Reset password with an invalid username.
    *   Reset password with an empty username.
    *   Verify error messages for invalid username.
    *   Verify password reset confirmation message.
*   **Social Media Links:**
    *   Verify social media icons are visible.
    *   Verify social media links navigate to the correct pages.
*   **Login Page Elements:**
    *   Verify all elements on the login page are displayed correctly (username field, password field, login button, etc.).

## Test Deliverables

*   Test Plan document
*   Test Cases (Gherkin feature files)
*   Test Execution Reports

## Environment

*   Browser: Chrome, Firefox, Edge
*   Operating System: Windows, macOS, Linux
*   Test Framework: Playwright

## Roles and Responsibilities

*   QA Architect: Responsible for creating and maintaining the test plan and test strategy.
*   QA Engineers: Responsible for writing and executing test cases, and reporting defects.

