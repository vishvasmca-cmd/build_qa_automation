# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be automated using a suitable testing framework.

## Scope

The scope of this test plan includes:

*   Smoke tests to verify core functionality.
*   Regression tests to ensure existing functionality remains intact after changes.

## Test Suites

1.  **Smoke Suite:** A minimal set of tests to verify the most critical functions.
2.  **Regression Suite:** A comprehensive suite of tests covering various scenarios and edge cases.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following 8-point checklist:

1.  **Critical Paths:** Tests cover essential user flows like searching for a product and initiating the checkout process.
2.  **Core Business Logic:** Focus on testing the primary functionality of adding items to the cart and proceeding to checkout.
3.  **Positive Testing:** Primarily focuses on successful scenarios (e.g., valid search, adding to cart).
4.  **No Negative Testing:** Negative scenarios (e.g., invalid search) are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios and edge cases are reserved for the regression suite.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback.
7.  **Independent Tests:** Each test should be independent and not rely on the state of previous tests.
8.  **High Stability:** Tests should be reliable and not prone to false failures.

## Test Cases

Detailed test cases will be documented in the respective feature files.

## Test Environment

The tests will be executed against the production environment: `https://www.dyson.in/`.

## Test Data

Test data will be managed within the test scripts.

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline.

## Metrics

*   Test pass/fail rate
*   Test execution time

