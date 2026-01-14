# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The scope of this test plan covers the following functionalities:

*   Homepage
*   Product Search
*   Product Detail Page (PDP)

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. It will be executed after each build to ensure that the critical paths are working as expected. The smoke suite will include tests for:

*   Homepage load and basic elements visibility
*   Product search functionality
*   Product Detail Page (PDP) load and key elements visibility (e.g., Add to Cart button)

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like product search and PDP loading.
2.  **Core Business Logic:** Focuses on verifying the search functionality, a core aspect of an e-commerce site.
3.  **Positive Testing:** Only positive scenarios are included (e.g., successful search, PDP load).
4.  **No Negative Testing:** Negative scenarios like invalid search terms are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios or boundary conditions are not included.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
7.  **Independent Tests:** Each test is independent and does not rely on the state of other tests.
8.  **High Stability:** Tests are reliable and not prone to flakiness.

### Regression Suite

The regression suite will provide comprehensive test coverage of the application. It will be executed periodically to ensure that new changes have not introduced any regressions. The regression suite will include tests for:

*   All functionalities covered in the smoke suite.
*   Alternative flows (e.g., different search terms, different product categories).
*   Negative scenarios (e.g., invalid search terms, out-of-stock products).
*   Boundary analysis (e.g., maximum quantity of products in the cart).
*   Cross-module interactions (e.g., search suggestions, related products).
*   Validation messages (e.g., error messages for invalid input).

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/macOS
*   Test Framework: Playwright
*   Test Runner: Jest

## Test Data

Test data will be used to simulate different user scenarios. This will include:

*   Valid search terms (e.g., Dyson V15 Detect).
*   Invalid search terms (e.g., gibberish).
*   Product categories (e.g., Vacuum Cleaners, Hair Care).

## Test Execution

*   Smoke tests will be executed after each build.
*   Regression tests will be executed periodically (e.g., nightly or weekly).
*   Test results will be reported in a clear and concise manner.

## Test Reporting

Test results will be reported using a test management tool. The reports will include:

*   Test execution status (pass/fail).
*   Test execution time.
*   Error messages (if any).
*   Screenshots (if any).

## Metrics

The following metrics will be used to track the progress and effectiveness of the testing effort:

*   Number of tests executed.
*   Number of tests passed.
*   Number of tests failed.
*   Test coverage.
*   Defect density.

