# Test Plan: core_orangehrm

## Introduction

This document outlines the test plan for the core_orangehrm project, focusing on verifying key functionalities of the OrangeHRM SaaS platform. The tests will cover login page elements, the 'Forgot your password?' link, and social media icons on the login page.

## Scope

The testing will cover the following areas:

*   Verification of login page elements (username, password fields, login button).
*   Functionality of the 'Forgot your password?' link.
*   Verification of social media icons on the login page.

## Test Strategy

The testing will be divided into Smoke and Regression test suites.

*   **Smoke Suite:**  A high-level suite to ensure the core functionality is working.
*   **Regression Suite:** A more comprehensive suite to cover edge cases and ensure no regressions are introduced.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following 8-point checklist:

1.  **Critical Path Focus:** Tests will focus on the most critical paths (e.g., accessing the login page, password reset).
2.  **Core Business Logic:** Verify the basic functionality of password reset.
3.  **Positive Testing:** Primarily positive testing (e.g., successful navigation).
4.  **No Negative Testing:** No negative testing in the smoke suite.
5.  **Minimal Edge Cases:** Avoid complex edge cases.
6.  **Fast Execution:** Tests should be quick to execute.
7.  **Build Validation:** Used to validate new builds.
8.  **Limited Scope:** Only cover essential functionalities.

## Test Suites

### Smoke Suite

*   Verify the login page is accessible.
*   Verify the 'Forgot your password?' link navigates to the password reset page.
*   Verify the user can enter a username on the password reset page and submit the reset request.
*   Verify navigation back to the login page.

### Regression Suite

*   (To be expanded based on further analysis and feature development)

## Test Environment

The tests will be executed against the following environment:

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/macOS
*   URL: https://opensource-demo.orangehrmlive.com/

## Test Deliverables

*   Test Plan document
*   Gherkin feature files
*   Test execution reports
