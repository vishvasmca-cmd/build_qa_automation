# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, a SaaS platform. The plan includes smoke and regression testing strategies to ensure the quality and stability of the application.

## Test Scope

The testing will cover the following areas:

*   Login page elements verification
*   'Forgot your password?' link functionality
*   Social media icons visibility and functionality

## Testing Strategy

### Smoke Suite Strategy

The smoke suite will focus on verifying the core functionality of the application. The following checklist will be applied:

1.  **Critical Paths:** Tests cover the most common and critical user flows.
2.  **Core Business Logic:** Focus on testing the primary business functions.
3.  **Positive Testing:** Primarily positive test cases are included.
4.  **Minimal Data Set:** Use a small, representative set of test data.
5.  **Fast Execution:** Tests should be quick to execute.
6.  **Build Acceptance:** Used to determine if a build is stable enough for further testing.
7.  **High Priority:** Smoke tests are given the highest priority.
8.  **Limited Scope:** Only essential functionalities are covered.

### Regression Suite Strategy

The regression suite will cover a broader range of functionalities, including alternative flows, negative scenarios, and boundary conditions. This suite aims to ensure that new changes have not introduced any regressions in existing functionalities.

## Test Suites

1.  Smoke Suite: Verifies the basic functionality of the login page, password reset, and social media links.
2.  Regression Suite: Includes more detailed test cases for all functionalities, including edge cases and error handling.

## Test Environment

*   **Browser:** Chrome, Firefox, Edge
*   **Operating System:** Windows, macOS, Linux
*   **URL:** https://opensource-demo.orangehrmlive.com/

## Test Deliverables

*   Test Plan Document
*   Test Cases (Gherkin Feature Files)
*   Test Execution Reports

