# Test Plan: core_automation_exercise

## Introduction

This document outlines the test plan for the core_automation_exercise project, focusing on the e-commerce domain. The plan includes smoke and regression test suites designed to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as product browsing, searching, adding items to the cart, and proceeding to checkout.

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. These tests are designed to be executed quickly and efficiently to ensure that the basic functionalities are working as expected.

#### Smoke Suite Strategy

The Smoke Suite Strategy for this project follows an 8-point checklist to ensure comprehensive coverage of critical functionalities:

1.  **Critical Paths:** Tests cover essential user flows like navigating to products, searching, adding to cart, and checkout.
2.  **Core Business Logic:** Focuses on verifying the primary operations related to product search and cart management.
3.  **Positive Testing:** Primarily uses valid inputs and scenarios to confirm expected behavior.
4.  **No Negative Testing:** Excludes tests with invalid inputs or error conditions in the smoke suite.
5.  **No Complex Edge Cases:** Avoids intricate scenarios or boundary conditions.
6.  **Prioritized Scenarios:** Concentrates on the most frequently used and critical functionalities.
7.  **Fast Execution:** Designed for quick execution to provide rapid feedback on build stability.
8.  **Build Validation:** Used to determine whether a build is stable enough for further testing.

### Regression Suite

The regression suite will include a more comprehensive set of tests to ensure that new changes have not introduced any regressions. This suite will cover a wider range of scenarios, including edge cases and negative tests.

## Test Modules

### Product Catalog

*   **Smoke:**
    *   Verify navigation to the Products page.
    *   Verify searching for a product.
*   **Regression:**
    *   Verify filtering products by category.
    *   Verify sorting products by price.
    *   Verify handling of search for non-existent products.

### Shopping Cart

*   **Smoke:**
    *   Verify adding a product to the cart.
    *   Verify viewing the cart summary.
*   **Regression:**
    *   Verify updating the quantity of items in the cart.
    *   Verify removing items from the cart.
    *   Verify handling of adding out-of-stock items.
    *   Verify cart persistence after page refresh.

### Checkout & Payments

*   **Smoke:**
    *   Verify proceeding to checkout.
*   **Regression:**
    *   Verify checkout with different address formats.
    *   Verify applying valid and invalid coupon codes.
    *   Verify handling of payment declines.
    *   Verify correct calculation of tax and shipping.
