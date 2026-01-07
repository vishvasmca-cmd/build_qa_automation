# Test Plan: core_saucedemo

## Overview

This test plan outlines the testing strategy for the core_saucedemo e-commerce application. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Test Suites

### Smoke Suite

The smoke suite focuses on verifying the core functionality of the application. It includes tests for login, sorting products, and adding items to the cart.

#### Smoke Suite Strategy

The following checklist was applied when designing the smoke suite:

1.  **Critical Paths:** Tests cover the most critical user flows (e.g., login, add to cart).
2.  **Core Business Logic:** Focuses on essential e-commerce functions.
3.  **Positive Testing:** Primarily uses valid inputs and expected outcomes.
4.  **No Negative Testing:** Excludes tests with invalid inputs or error conditions.
5.  **No Complex Edge Cases:** Avoids intricate scenarios or boundary conditions.
6.  **Speed:** Tests are designed to execute quickly.
7.  **Independence:** Tests are independent and do not rely on each other.
8.  **Automation Feasibility:** Tests are easily automatable.

### Regression Suite

The regression suite provides comprehensive test coverage, including alternative flows, negative scenarios, and boundary conditions.

## Test Modules

### Authentication

*   Smoke: User Login (Valid)
*   Regression: Login with Invalid Password, Password Reset Flow

### Product Catalog

*   Smoke: View Product Details, Search for standard product
*   Regression: Filter products by Price/Category, Sort products (Price Low-High), Search for non-existent product

### Shopping Cart

*   Smoke: Add Item to Cart, View Cart Summary
*   Regression: Update Quantity in Cart, Remove Item from Cart, Add Out-of-Stock Item (Verify Error)

### Checkout & Payments

*   Smoke: Complete Purchase (Guest / Standard)
*   Regression: Checkout with formatted Address, Apply Valid/Invalid Coupon Code, Payment Decline Simulation, Calculate Tax/Shipping correctly