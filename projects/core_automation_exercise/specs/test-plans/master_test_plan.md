# Test Plan: core_automation_exercise

## Introduction

This document outlines the test plan for the core_automation_exercise project, focusing on the e-commerce domain. The plan includes smoke and regression test suites designed to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as product browsing, searching, adding to cart, and proceeding to checkout.

## Test Suites

### Smoke Suite

The smoke suite will focus on critical path testing to ensure the core functionalities are working as expected.  If these tests fail, the build should be rejected.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover the most important user flows (e.g., login, checkout).
2.  **Core Business Logic:** Focus on primary revenue or operational flows.
3.  **Positive Testing:** Primarily happy path scenarios are included.
4.  **No Negative Testing:**  Error handling is generally excluded from smoke tests.
5.  **No Complex Edge Cases:** Complex scenarios and boundary conditions are avoided.
6.  **Fast Execution:** Tests are designed to run quickly to provide rapid feedback.
7.  **Independent Tests:** Each test should be independent and not rely on others.
8.  **Limited Scope:** The suite covers a minimal set of functionalities.

#### Smoke Test Cases

*   **Product Search and Checkout:**
    *   Navigate to the Products page.
    *   Search for a product ('Dress').
    *   Add the product to the cart.
    *   Proceed to checkout.

### Regression Suite

The regression suite will include a more comprehensive set of tests to cover various scenarios, edge cases, and error handling. This suite ensures that new changes haven't introduced regressions in existing functionality.

#### Regression Test Cases

*   **Product Catalog:**
    *   Filter products by price and category.
    *   Sort products by price (low to high).
    *   Search for a non-existent product.
    *   Verify pagination.
*   **Shopping Cart:**
    *   Update quantity in cart.
    *   Remove item from cart.
    *   Add out-of-stock item and verify error message.
    *   Verify cart persistence after page refresh.
*   **Checkout & Payments:**
    *   Checkout with different address formats.
    *   Apply valid and invalid coupon codes.
    *   Simulate payment decline.
    *   Verify correct calculation of tax and shipping.

## Test Environment

*   Browser: Chrome, Firefox
*   Operating System: Windows, macOS, Linux
*   Test Data: Use a combination of valid and invalid test data.

## Test Execution

*   Smoke tests will be executed after each build.
*   Regression tests will be executed before each release.

