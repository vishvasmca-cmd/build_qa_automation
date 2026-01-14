# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The tests will be automated using Playwright and follow Behavior-Driven Development (BDD) principles.

## Scope

The scope of this test plan includes:

*   Smoke tests to verify core functionality.
*   Regression tests to ensure existing functionality remains intact after changes.

## Test Environment

*   Browser: Chromium (latest version)
*   Operating System: Windows/macOS/Linux (cross-platform)
*   Test Framework: Playwright
*   Language: JavaScript/TypeScript

## Test Suites

### Smoke Suite

The smoke suite will cover the most critical user flows to ensure the basic functionality of the Dyson India website is working as expected. This includes:

*   Homepage load and basic element presence.
*   Product search and navigation to the product details page (PDP).
*   Adding a product to the cart and proceeding to checkout.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** The smoke tests cover the core user journey of searching for a product and adding it to the cart.
2.  **Core Business Logic:** The ability to search and add items to the cart is fundamental to an e-commerce site.
3.  **Positive Testing:** The smoke tests focus on the happy path, assuming valid inputs and successful operations.
4.  **No Negative Testing:** Negative scenarios like invalid search queries are excluded from the smoke suite.
5.  **No Complex Edge Cases:** The smoke tests do not cover edge cases like out-of-stock items or promotional discounts.
6.  **Fast Execution:** The smoke tests are designed to be quick and efficient, providing rapid feedback on build stability.
7.  **Independent Tests:** Each smoke test is independent and can be run in isolation.
8.  **Limited Scope:** The smoke suite is limited to the essential functionalities required for a basic e-commerce transaction.

### Regression Suite

The regression suite will cover a broader range of scenarios, including alternative flows, negative tests, and edge cases. This will ensure that new changes do not introduce regressions in existing functionality. This includes:

*   Alternative search methods (e.g., using different keywords, filters).
*   Handling out-of-stock items.
*   Validating error messages for invalid inputs.
*   Testing different payment methods (if applicable).
*   Verifying cross-module interactions (e.g., cart updates reflected in the header).

## Test Cases

Test cases will be written in Gherkin syntax and stored in feature files. Each test case will have a clear description, preconditions, steps, and expected results.

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Test results will be reported in a clear and concise manner, including pass/fail status, execution time, and error messages (if any).

## Metrics

The following metrics will be tracked to monitor the effectiveness of the testing process:

*   Number of tests executed.
*   Number of tests passed.
*   Number of tests failed.
*   Test execution time.
*   Defect density.

## Tools

*   Playwright: For test automation.
*   GitHub: For version control and collaboration.
*   CI/CD Pipeline (e.g., Jenkins, GitHub Actions): For automated test execution.

