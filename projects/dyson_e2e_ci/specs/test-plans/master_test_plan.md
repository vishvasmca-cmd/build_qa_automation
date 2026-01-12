# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as product search, adding to cart, and navigating to the checkout page. The tests will be executed against the production environment (https://www.dyson.in/).

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. It will be executed after each build to ensure that the critical paths are working as expected. If any of the smoke tests fail, the build will be rejected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** The smoke tests cover the most critical user flows, such as searching for a product, adding it to the cart, and navigating to the checkout page.
2.  **Core Business Logic:** The tests verify the core business logic related to product search and cart management.
3.  **Positive Testing:** The smoke tests primarily focus on positive scenarios, ensuring that the happy paths are working correctly.
4.  **No Negative Testing:** Negative testing is excluded from the smoke suite to keep it focused on the most critical functionalities.
5.  **No Complex Edge Cases:** Complex edge cases are not included in the smoke suite to maintain its simplicity and speed.
6. **Limited Data Variation:** Smoke tests use a minimal set of data to validate core functionality, avoiding extensive data combinations.
7. **Independent Tests:** Each smoke test is designed to be independent, minimizing dependencies between tests.
8. **Fast Execution:** The smoke tests are designed to execute quickly, providing rapid feedback on the build's health.

### Regression Suite

The regression suite will provide comprehensive test coverage of the application. It will include alternative flows, negative scenarios, boundary analysis, cross-module interactions, and validation messages.

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. The feature files will be organized by functionality.

## Test Environment

*   **URL:** https://www.dyson.in/
*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10

## Test Execution

The tests will be executed using a CI/CD pipeline. The smoke tests will be executed after each build, and the regression tests will be executed on a nightly basis.

## Test Reporting

Test results will be reported using a test reporting tool. The reports will include the status of each test case, the execution time, and any error messages.
