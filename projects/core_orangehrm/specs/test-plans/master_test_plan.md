# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, focusing on verifying login page elements, the 'Forgot your password?' link functionality, and the visibility of social media icons on the login page.

## Scope

The scope of this test plan includes:

*   Verification of login page elements (username, password fields, login button).
*   Functionality of the 'Forgot your password?' link, including navigation to the password reset page and the ability to initiate a password reset.
*   Visibility of social media icons on the login page.

## Test Strategy

This test plan will employ both smoke and regression testing strategies to ensure the quality and stability of the core_orangehrm application.

### Smoke Suite Strategy

The smoke suite will focus on the critical path of password reset functionality. The following 8-point checklist has been applied to define the smoke suite:

1.  **Critical Paths:** The 'Forgot Password' flow is a critical path.
2.  **Core Business Logic:** Password reset is essential for user access.
3.  **Positive Testing:** Focus on successful password reset initiation.
4.  **No Negative Testing:** No invalid username attempts in smoke.
5.  **No Complex Edge Cases:** Standard password reset flow only.
6.  **Fast Execution:** Smoke tests should be quick to execute.
7.  **Independent Tests:** Tests should be independent of each other.
8.  **Automated:** The smoke tests will be automated.

### Regression Suite Strategy

The regression suite will cover a broader range of scenarios, including:

*   Negative scenarios for the 'Forgot your password?' functionality (e.g., invalid username).
*   Verification of error messages.
*   Cross-browser compatibility testing.
*   Testing of social media icon links.

## Test Suites

1.  **Smoke Suite:**
    *   Verify the 'Forgot your password?' link navigates to the password reset page.
    *   Initiate a password reset request with a valid username.
    *   Verify navigation back to the login page from the password reset confirmation page.
2.  **Regression Suite:**
    *   Verify the presence and functionality of all login page elements.
    *   Verify error messages for invalid username during password reset.
    *   Verify the visibility and correct links of social media icons on the login page.

## Test Cases

(Detailed test cases will be documented separately, based on the above test suites.)
