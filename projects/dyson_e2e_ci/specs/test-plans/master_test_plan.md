# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user workflows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The tests will cover key functionalities such as:

*   Handling popups
*   Searching for products
*   Verifying product details page elements

## Test Suites

### Smoke Suite

The smoke suite will focus on the core functionality of the Dyson website.  It will verify that the most critical paths are functioning correctly.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Includes essential user flows like product search and basic PDP verification.
2.  **Core Business Logic:** Focuses on the primary function of an e-commerce site: finding and viewing products.
3.  **No Negative Testing:**  Excludes tests with invalid inputs or error conditions.
4.  **No Complex Edge Cases:** Avoids tests that explore unusual or boundary conditions.
5.  **Minimal Test Data:** Uses a small, representative set of data for testing.
6.  **Fast Execution:** Designed to run quickly to provide rapid feedback on build stability.
7.  **Independent Tests:** Each test should be independent and not rely on the state of other tests.
8.  **Clear Pass/Fail Criteria:**  Each test has a well-defined expected outcome.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, and edge cases. This suite will ensure that new changes haven't introduced regressions in existing functionality. (Note: Based on the limited trace data, a detailed regression suite cannot be fully defined.  This would require a more complete user journey.)

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System:  Platform independent (Windows, macOS, Linux)
*   Test Framework: Playwright

## Test Deliverables

*   Test Plan Document
*   Gherkin Feature Files
*   Test Execution Reports

