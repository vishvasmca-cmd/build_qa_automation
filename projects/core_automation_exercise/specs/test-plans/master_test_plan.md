# Test Plan: core_automation_exercise

## Introduction

This document outlines the test plan for the core_automation_exercise project, focusing on the e-commerce domain. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as product browsing, searching, adding to cart, and proceeding to checkout. The tests will be executed against the https://automationexercise.com/ website.

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. These tests are designed to be quick and efficient, providing a high level of confidence in the stability of the system.

#### Smoke Suite Strategy

The smoke suite strategy for this project follows an 8-point checklist to ensure comprehensive coverage of critical functionalities:

1.  **Critical Path Coverage**: Tests cover the most common and essential user flows (e.g., product search, add to cart, checkout).
2.  **Core Functionality**: Focus on testing the primary functions of each module (e.g., product details, cart operations).
3.  **Positive Testing**: Primarily uses valid and expected inputs to confirm correct behavior.
4.  **No Negative Testing**: Excludes tests with invalid or malicious inputs in the smoke suite.
5.  **Minimal Edge Cases**: Avoids complex or rare scenarios.
6.  **Fast Execution**: Tests are designed for quick execution to provide rapid feedback.
7.  **Independent Tests**: Each test operates independently without relying on the state of others.
8.  **High Priority**: Any failures in the smoke suite are treated as critical and require immediate attention.

#### Smoke Test Cases

*   Navigate to Products page
*   Search for a product ('Dress')
*   Add a product to the cart
*   View the cart
*   Proceed to checkout

### Regression Suite

The regression suite will include a more comprehensive set of tests to ensure that new changes have not introduced any regressions. This suite will cover a wider range of scenarios, including edge cases and negative tests.

#### Regression Test Cases

*   Search for a non-existent product
*   Attempt to add an out-of-stock item to the cart
*   Verify cart persistence after refreshing the page
*   Apply a valid and invalid coupon code during checkout
*   Simulate a payment decline during checkout

## Test Environment

*   **URL**: https://automationexercise.com/
*   **Browsers**: Chrome, Firefox
*   **Operating Systems**: Windows, macOS

## Test Execution

The tests will be executed using a CI/CD pipeline. The smoke tests will be executed on every commit, while the regression tests will be executed on a nightly basis.

## Test Reporting

Test results will be reported using a centralized test management system. The reports will include detailed information about each test case, including the status, execution time, and any errors encountered.
