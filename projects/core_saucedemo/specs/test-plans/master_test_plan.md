# Test Plan: core_saucedemo

## Introduction

This document outlines the test plan for the core_saucedemo e-commerce application. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The testing will cover the following modules:

*   Authentication
*   Product Catalog
*   Shopping Cart
*   Checkout & Payments

## Test Suites

### Smoke Suite

The smoke suite will focus on the critical paths and core functionalities of the application. It will be executed to ensure that the basic functionalities are working as expected.

#### Smoke Suite Strategy

The following checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Include tests for the most important user flows (e.g., login, checkout).
2.  **Core Business Logic:** Verify the primary revenue or operational flows.
3.  **Positive Testing:** Focus on happy path scenarios with valid inputs.
4.  **No Negative Testing:** Exclude tests with invalid inputs or error conditions (unless critical security).
5.  **No Complex Edge Cases:** Avoid complex scenarios or boundary conditions.
6.  **Fast Execution:** Design tests that can be executed quickly to provide rapid feedback.
7.  **Independent Tests:** Ensure tests are independent and do not rely on each other.
8.  **Limited Scope:** Keep the scope of each test focused and minimal.

### Regression Suite

The regression suite will cover a broader range of scenarios, including alternative flows, negative scenarios, and boundary conditions. It will be executed to ensure that new changes have not introduced any regressions.

## Test Modules and Coverage

### Module: Authentication (Criticality: High)

*   **Smoke Tests:**
    *   User Login (Valid)

*   **Regression Tests:**
    *   Login with Invalid Password
    *   Login with Locked Account
    *   Password Reset Flow
    *   Registration with Existing Email

### Module: Product Catalog (Criticality: Medium)

*   **Smoke Tests:**
    *   View Product Details
    *   Search for standard product

*   **Regression Tests:**
    *   Filter products by Price/Category
    *   Sort products (Price Low-High)
    *   Search for non-existent product
    *   Verify Pagination

### Module: Shopping Cart (Criticality: High)

*   **Smoke Tests:**
    *   Add Item to Cart
    *   View Cart Summary

*   **Regression Tests:**
    *   Update Quantity in Cart
    *   Remove Item from Cart
    *   Add Out-of-Stock Item (Verify Error)
    *   Cart Persistence (Refresh Page)

### Module: Checkout & Payments (Criticality: Critical)

*   **Smoke Tests:**
    *   Complete Purchase (Guest / Standard)

*   **Regression Tests:**
    *   Checkout with formatted Address
    *   Apply Valid/Invalid Coupon Code
    *   Payment Decline Simulation
    *   Calculate Tax/Shipping correctly
