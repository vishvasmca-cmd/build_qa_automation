# Test Plan: core_saucedemo

## Introduction

This document outlines the test plan for the core_saucedemo e-commerce application. It details the testing scope, strategy, and specific test cases to be executed.

## Test Scope

The testing will cover the following modules:

*   Authentication (Login/Logout)
*   Product Catalog (Sorting)
*   Shopping Cart (Add to Cart)

## Test Strategy

We will employ a two-pronged testing approach:

1.  **Smoke Testing:** To ensure the core functionality is working after each build.
2.  **Regression Testing:** To ensure that new changes haven't introduced bugs into existing functionality.

### Smoke Suite Strategy

The Smoke Suite will adhere to the following checklist:

1.  Critical Paths: Focus on essential user flows.
2.  Core Business Logic: Verify the primary functions of the application.
3.  Positive Testing: Primarily happy path scenarios.
4.  No Negative Testing: Unless critical security concerns exist.
5.  No Complex Edge Cases: Keep the scenarios straightforward.
6.  Speed: Tests should execute quickly to provide rapid feedback.
7.  Stability: Tests should be reliable and not prone to flakiness.
8.  Independence: Tests should be independent of each other.

## Test Suites

### Smoke Suite

The Smoke Suite will include the following test cases:

*   Successful user login.
*   Sorting products by price (low to high).
*   Adding a product to the cart.

### Regression Suite

The Regression Suite will include a more comprehensive set of test cases, covering:

*   Authentication:
    *   Invalid login attempts.
    *   Password reset flow.
*   Product Catalog:
    *   Filtering products by category.
    *   Searching for products.
*   Shopping Cart:
    *   Updating quantity in cart.
    *   Removing items from cart.
*   Checkout & Payments:
    *   Completing purchase with different payment methods.
    *   Applying coupon codes.

