# Test Plan: core_orangehrm

## Introduction

This test plan outlines the testing strategy for the core_orangehrm application, focusing on verifying key functionalities and ensuring application stability. The plan includes both smoke and regression test suites.

## Scope

The testing will cover the following areas:

*   Login Page Elements
*   Forgot Password Functionality
*   Social Media Icons on Login Page

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities of the application are working as expected. This includes verifying the presence of login page elements and the functionality of the 'Forgot your password?' link.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover the most important user flows (e.g., login, password reset).
2.  **Core Business Logic:** Focuses on essential functionalities related to user authentication.
3.  **Positive Testing:** Primarily focuses on successful scenarios (e.g., valid password reset request).
4.  **No Negative Testing:** Excludes tests for invalid inputs or error conditions in this initial suite.
5.  **No Complex Edge Cases:** Avoids complex scenarios or boundary conditions.
6.  **Fast Execution:** Tests are designed to be quick and efficient.
7.  **Build Verification:** Used to determine if a build is stable enough for further testing.
8.  **Limited Scope:** Covers only the most vital functionalities.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions. This will ensure that new changes have not introduced any regressions in existing functionalities.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each test case will have a clear description, preconditions, steps, and expected results.

## Test Environment

The tests will be executed in a dedicated test environment that mirrors the production environment. This will ensure that the test results are accurate and reliable.

## Test Deliverables

*   Test Plan Document
*   Gherkin Feature Files
*   Test Execution Reports
*   Defect Reports

## Roles and Responsibilities

*   QA Architect: Responsible for creating and maintaining the test plan, designing the test suites, and providing guidance to the test team.
*   Test Engineers: Responsible for writing and executing test cases, reporting defects, and verifying fixes.

## входные и выходные данные

*   Input: Trace data, domain, and project name.
*   Output: Test plan content and Gherkin feature files.
