# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The testing will cover key functionalities such as:

*   Handling popups
*   Product search
*   Product detail page (PDP) verification
*   Add to cart functionality
*   Checkout process

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. These tests are designed to be executed quickly and efficiently to ensure that the main features are working as expected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover essential user flows like product search, adding to cart, and initiating checkout.
2.  **Core Business Logic:** Focuses on verifying the basic functionality of adding a product to the cart and proceeding to checkout.
3.  **Positive Testing:** Primarily includes positive test scenarios, ensuring that the happy path flows work correctly.
4.  **No Negative Testing:** Negative scenarios (e.g., invalid input) are excluded from the smoke suite.
5.  **No Complex Edge Cases:** Complex scenarios and edge cases are reserved for the regression suite.
6.  **Fast Execution:** Tests are designed to execute quickly to provide rapid feedback on the application's health.
7.  **Independent Tests:** Each test is independent and does not rely on the state of other tests.
8.  **Minimal Data Setup:** Tests require minimal data setup to reduce complexity and execution time.

### Regression Suite

The regression suite will include a more comprehensive set of tests to ensure that new changes have not introduced any regressions. This suite will cover alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/11, macOS
*   **Test Framework:** Playwright
*   **Test Language:** JavaScript

## Test Data

Test data will be used to simulate various user scenarios and ensure that the application behaves as expected. This will include:

*   Valid search queries (e.g., "Dyson V15 Detect")
*   Valid product selections

## Test Deliverables

*   Test Plan Document
*   Test Scripts (Playwright)
*   Test Results
*   Defect Reports

## Test Execution

The tests will be executed automatically as part of the CI/CD pipeline. The results will be monitored to identify any failures and ensure that they are addressed promptly.
