# Test Plan: core_saucedemo

## Overview

This test plan outlines the testing strategy for the core_saucedemo e-commerce application. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Test Suites

### Smoke Suite

The smoke suite focuses on verifying the core functionality of the application. It includes tests for login, product sorting, adding items to the cart, and checkout.

#### Smoke Suite Strategy

The following checklist was applied when designing the smoke suite:

1.  **Critical Paths:** Tests cover the most common user flows (e.g., login, checkout).
2.  **Core Business Logic:** Tests validate essential business rules (e.g., product pricing).
3.  **Positive Testing:** Focus on successful scenarios (e.g., valid login).
4.  **Minimal Complexity:** Avoid complex edge cases or variations.
5.  **Fast Execution:** Tests should be quick to execute for rapid feedback.
6.  **Independent Tests:** Tests should be independent and not rely on each other.
7.  **High Priority:** Smoke tests are the highest priority and must pass for a build to be considered stable.
8.  **Automated:** All smoke tests should be automated.

### Regression Suite

The regression suite provides comprehensive coverage of the application's functionality. It includes tests for alternative flows, negative scenarios, boundary conditions, and cross-module interactions.

## Test Modules

### Authentication

*   Smoke: User Login (Valid)
*   Regression: Login with Invalid Password, Password Reset Flow

### Product Catalog

*   Smoke: View Product Details, Search for standard product
*   Regression: Filter products by Price/Category, Search for non-existent product

### Shopping Cart

*   Smoke: Add Item to Cart, View Cart Summary
*   Regression: Update Quantity in Cart, Remove Item from Cart

### Checkout & Payments

*   Smoke: Complete Purchase (Guest / Standard)
*   Regression: Checkout with formatted Address, Apply Valid/Invalid Coupon Code
