# Test Plan: core_orangehrm

## Introduction

This document outlines the test plan for the core_orangehrm project, focusing on the login page elements, 'Forgot your password?' functionality, and social media icons.

## Scope

The testing will cover the following areas:

*   Verification of login page elements.
*   Functionality of the 'Forgot your password?' link.
*   Visibility of social media icons on the login page.

## Test Strategy

We will employ both smoke and regression testing strategies.

### Smoke Suite Strategy

The smoke suite will focus on the core functionality of the login page. The following 8-point checklist has been applied:

1.  **Critical Path Coverage:** Tests cover the most common user flow (attempting to reset password).
2.  **Positive Testing:** Focus is on successful password reset flow.
3.  **No Negative Testing:**  Invalid username scenarios are excluded from smoke tests.
4.  **Minimal Data Variation:** Only one username is used for the reset password flow.
5.  **No Edge Cases:**  Boundary conditions or unusual inputs are not covered.
6.  **Fast Execution:**  Tests are designed for quick execution to provide rapid feedback.
7.  **Independent Tests:**  Tests are independent and can be run in any order.
8.  **Automated:**  The smoke suite is fully automated.

### Regression Suite Strategy

The regression suite will provide comprehensive coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

## Test Suites

1.  **Smoke Suite:**
    *   Verify 'Forgot your password?' link functionality.
    *   Verify username field on password reset page.
    *   Verify 'Reset Password' button functionality.
    *   Verify navigation back to login page.
    *   Verify social media icons are visible on the login page.

2.  **Regression Suite:**
    *   All smoke tests.
    *   Negative tests for invalid username on password reset page.
    *   Verify error messages for invalid username.
    *   Verify all login page elements are present and functional.
    *   Verify all social media icons are present and link to the correct pages.

## Test Deliverables

*   Test Plan document
*   Test Cases (Gherkin feature files)
*   Test Automation Scripts
*   Test Execution Reports

