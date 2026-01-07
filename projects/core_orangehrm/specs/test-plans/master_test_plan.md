# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, focusing on verifying key functionalities and ensuring application stability. The application falls under the SaaS domain.

## Scope

The testing will cover the following areas:

*   Login page elements verification
*   'Forgot your password?' link functionality
*   Social media icons visibility and functionality

## Test Strategy

The testing will be divided into two main suites: Smoke and Regression.

*   **Smoke Suite:** A high-level suite to verify the core functionalities.
*   **Regression Suite:** A comprehensive suite to ensure that new changes haven't introduced regressions.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following checklist:

1.  **Critical Paths:** Focus on the most critical user flows (e.g., login).
2.  **Core Business Logic:** Verify the primary business functions.
3.  **Positive Testing:** Primarily focus on positive test cases.
4.  **No Negative Testing:** Exclude negative test cases unless they are critical for security.
5.  **Minimal Edge Cases:** Avoid complex edge cases in the smoke suite.
6.  **Fast Execution:** Design tests for quick execution to provide rapid feedback.
7.  **Build Validation:** Use the smoke suite to validate new builds.
8.  **Essential Functionality:** Cover only the essential functionality required for basic operation.

### Regression Suite Strategy

### 1. Smoke Suite

*   Verify login page elements are present.
*   Verify 'Forgot your password?' link navigates to the password reset page.
*   Verify social media icons are visible on the login page and navigate to the correct pages.

### 2. Regression Suite

*   Verify all login page elements, including labels, input fields, and buttons.
*   Test the 'Forgot your password?' link with valid and invalid usernames.
*   Verify the password reset process.
*   Verify all social media icons navigate to the correct pages.
*   Test login with valid and invalid credentials.
*   Test the application's response to various error conditions.

## Test Deliverables

*   Test Plan document
*   BDD Feature files (Gherkin syntax)
*   Test execution reports

## Environment

The tests will be executed on the following environment:

*   Browser: Chrome
*   Operating System: Windows/macOS
*   Test Framework: Playwright

## Entry Criteria

*   The application is deployed and accessible in the test environment.
*   Test data is available.

## Exit Criteria

*   All planned tests have been executed.
*   All critical and high-priority defects have been resolved.
*   Test execution report is generated and approved.
