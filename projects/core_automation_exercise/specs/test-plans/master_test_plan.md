# Test Plan: core_automation_exercise

## Introduction

This document outlines the test plan for the core_automation_exercise project, focusing on the ecommerce domain. The plan includes smoke and regression test suites designed to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as product browsing, searching, adding items to the cart, and proceeding to checkout.

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities are working as expected. These tests will be executed on every build to quickly identify any major issues.

#### Smoke Suite Strategy

The smoke suite strategy for this project follows an 8-point checklist:

1.  **Critical Paths Only**: Focus solely on the most essential workflows (e.g., login, add to cart, checkout).
2.  **Positive Testing**: Primarily use valid/expected inputs.
3.  **Minimal Data**: Use a small, representative set of test data.
4.  **No Edge Cases**: Avoid complex scenarios or boundary conditions.
5.  **Independent Tests**: Each test should be able to run independently without relying on the state of others.
6.  **Fast Execution**: Tests should be designed for quick execution to provide rapid feedback.
7.  **Automated**: All smoke tests must be automated.
8.  **Build Breaker**: Failure of any smoke test should result in a failed build.

### Regression Suite

The regression suite will include a more comprehensive set of tests to cover various scenarios, edge cases, and negative testing. This suite will be executed periodically to ensure that new changes have not introduced any regressions.

## Test Modules

### Product Catalog

*   **Smoke:**
    *   Navigate to Products page
    *   Search for a product
*   **Regression:**
    *   Filter products by category
    *   Sort products by price
    *   Search for a non-existent product

### Shopping Cart

*   **Smoke:**
    *   Add item to cart
*   **Regression:**
    *   Update quantity in cart
    *   Remove item from cart
    *   Add out-of-stock item

### Checkout

*   **Smoke:**
    *   Proceed to checkout
*   **Regression:**
    *   Enter shipping information
    *   Apply coupon code
    *   Handle payment failures
