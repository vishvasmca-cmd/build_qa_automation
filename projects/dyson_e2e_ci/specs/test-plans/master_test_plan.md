# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The tests will cover key functionalities such as:

*   Homepage interactions (popup handling)
*   Product search and navigation
*   Product Detail Page (PDP) verification
*   Add to Cart functionality
*   Checkout process

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. These tests are designed to be executed quickly and efficiently to ensure that the system is in a stable state.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** The smoke tests cover the most critical user paths, such as product search, adding to cart, and initiating checkout.
2.  **Core Business Logic:** The tests validate the core business logic related to product availability and pricing.
3.  **Positive Testing:** The smoke tests primarily focus on positive scenarios, ensuring that the happy path flows work as expected.
4.  **No Negative Testing:** Negative testing is excluded from the smoke suite to maintain its focus on core functionality.
5.  **No Complex Edge Cases:** Complex edge cases are not included in the smoke suite to keep the tests simple and fast.
6.  **Minimal Data Variation:** The smoke tests use a minimal set of data to cover the essential scenarios.
7.  **Fast Execution:** The smoke tests are designed to execute quickly, providing rapid feedback on the system's health.
8.  **High Priority:** Smoke tests are given the highest priority and are executed before any other tests.

### Regression Suite

The regression suite will provide comprehensive test coverage to ensure that new changes do not introduce regressions into existing functionality. This suite will include a wider range of scenarios, including alternative flows, negative tests, and edge cases.

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/macOS
*   **Test Framework:** Playwright
*   **Test Language:** JavaScript

## Test Data

Test data will be used to simulate various user scenarios and ensure that the application behaves as expected under different conditions.

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Results will be reported to a central dashboard for analysis and tracking.
