# Test Plan: core_parabank

## Introduction

This document outlines the test plan for the core_parabank application, focusing on verifying the login page, checking the find transactions link, and navigating to the about us page. The test plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The scope of this test plan includes:

*   Verification of the login page.
*   Checking the functionality of the 'find transactions' link.
*   Navigation to the 'About Us' page.

## Test Suites

### Smoke Suite

The smoke suite will focus on the critical path to ensure the core functionality of the application is working as expected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover the most important user flows (e.g., login).
2.  **Core Business Logic:** Focuses on primary revenue/operation flows.
3.  **Positive Testing:** Primarily happy path scenarios.
4.  **No Negative Testing:** Unless critical security concerns exist.
5.  **No Complex Edge Cases:** Avoids intricate scenarios.
6.  **Fast Execution:** Designed for quick feedback on build stability.
7.  **Independent Tests:** Tests should not depend on each other.
8.  **Limited Scope:** Covers only essential functionalities.

#### Smoke Test Cases

*   Verify the login page is accessible.
*   Check the 'Account History' link navigates to the correct page.

### Regression Suite

The regression suite will include a more comprehensive set of tests to ensure that new changes have not introduced any regressions.

#### Regression Test Cases

*   Verify the login page is accessible.
*   Check the 'Account History' link navigates to the correct page.
*   Navigate to the 'About Us' page.

## Test Environment

The tests will be executed in a stable test environment that mirrors the production environment.

## Test Data

Test data will be used to simulate various scenarios and ensure the application handles different types of data correctly.

## Entry Criteria

*   The application build must be successfully deployed to the test environment.
*   All necessary test data must be available.

## Exit Criteria

*   All test cases in the smoke suite must pass.
*   A high percentage of test cases in the regression suite must pass.
*   All critical and high-priority defects must be resolved.
