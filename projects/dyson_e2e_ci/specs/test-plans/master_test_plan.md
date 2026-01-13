# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The testing will cover key functionalities such as product search, adding to cart, and navigating to the checkout page. The tests will be executed against the production environment (https://www.dyson.in/).

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. It will include tests for:

*   Handling popups
*   Searching for a product
*   Adding a product to the cart
*   Navigating to the checkout page

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** The smoke tests cover the most critical path of searching a product and navigating to checkout.
2.  **Core Business Logic:** Adding a product to cart and navigating to checkout is a core business logic.
3.  **No Negative Testing:** The smoke tests focus on happy path scenarios.
4.  **No Complex Edge Cases:** The smoke tests do not include complex edge cases.
5.  **Fast Execution:** The smoke tests are designed to execute quickly.
6.  **Independent Tests:** Each smoke test is independent of the others.
7.  **Clear Pass/Fail Criteria:** The smoke tests have clear pass/fail criteria.
8.  **Automated:** The smoke tests are automated.

### Regression Suite

The regression suite will include a more comprehensive set of tests to ensure that new changes have not introduced any regressions. It will include tests for:

*   Alternative search methods
*   Handling different types of products
*   Validating cart functionality
*   Testing different checkout options
*   Negative scenarios (e.g., invalid search terms)

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10/macOS
*   Test Framework: Playwright

## Test Execution

The tests will be executed automatically as part of the CI/CD pipeline. The results will be reported in a centralized test management system.

## Test Deliverables

*   Test Plan
*   Test Scripts
*   Test Results
*   Defect Reports
