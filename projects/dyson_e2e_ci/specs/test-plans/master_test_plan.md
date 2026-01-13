# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The primary focus of the tests is to validate the core functionalities of the Dyson India e-commerce platform, including:

*   Searching for products
*   Adding products to the cart
*   Navigating to the checkout page

## Test Suites

### Smoke Suite

The smoke suite is designed to quickly verify the critical functionalities of the application. It includes happy path scenarios and aims to identify major issues early in the development cycle.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** The smoke suite covers the most critical user flows, such as product search, add to cart, and checkout initiation.
2.  **Core Business Logic:** The tests validate the core business logic related to product availability and cart management.
3.  **No Negative Testing:** The smoke suite focuses on positive scenarios and does not include negative tests.
4.  **No Complex Edge Cases:** The tests avoid complex edge cases and focus on the most common user interactions.
5.  **Fast Execution:** The smoke tests are designed to execute quickly to provide rapid feedback.
6.  **Independent Tests:** Each smoke test is independent and can be executed in any order.
7.  **Minimal Dependencies:** The tests have minimal dependencies on external systems or data.
8.  **Clear Assertions:** The tests include clear assertions to verify the expected outcomes.

### Regression Suite

The regression suite is a comprehensive set of tests that covers a wide range of scenarios, including alternative flows, negative tests, and edge cases. It ensures that new changes do not introduce regressions in existing functionalities.

## Test Environment

*   **Browser:** Chrome (latest version)
*   **Operating System:** Windows 10/11, macOS
*   **Test Framework:** Playwright

## Test Data

Test data will be used to simulate various user scenarios and product configurations. This includes:

*   Valid and invalid search queries
*   Different product types and quantities

## Test Execution

Tests will be executed automatically as part of the CI/CD pipeline. Results will be reported to a central dashboard for analysis and tracking.

## Test Deliverables

*   Test Plan document
*   Test scripts (Playwright)
*   Test results reports

