# Test Plan: core_automation_exercise

## Introduction

This document outlines the test plan for the core_automation_exercise project, an e-commerce platform. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover key functionalities such as product browsing, searching, adding to cart, and checkout process.

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. These tests are designed to be executed quickly and efficiently to ensure that the basic functionalities are working as expected.

#### Smoke Suite Strategy

The Smoke Suite for this project adheres to the following 8-point checklist:

1.  **Critical Paths:** Tests cover essential user flows like product search, adding to cart, and initiating checkout.
2.  **Core Business Logic:** Focuses on verifying the basic functionality of adding items to the cart.
3.  **No Negative Testing:**  Excludes tests with invalid inputs or error conditions.
4.  **Happy Path Focus:**  Tests use valid data and follow the expected user journey.
5.  **Limited Scope:** Only the most important functionalities are included.
6.  **Speed of Execution:** Tests are designed to run quickly to provide rapid feedback.
7.  **Build Validation:**  Aims to quickly determine if a build is stable enough for further testing.
8.  **Automated Execution:** Designed for automated execution as part of the CI/CD pipeline.

### Regression Suite

The regression suite will cover a broader range of functionalities, including edge cases, alternative flows, and negative scenarios. This suite ensures that new changes have not introduced any regressions in existing functionalities.

## Test Modules

### Authentication (High)

*   Smoke: User Login (Valid), User Registration (Happy Path)
*   Regression: Login with Invalid Password, Login with Locked Account, Password Reset Flow, Registration with Existing Email

### Product Catalog (Medium)

*   Smoke: View Product Details, Search for standard product
*   Regression: Filter products by Price/Category, Sort products (Price Low-High), Search for non-existent product, Verify Pagination

### Shopping Cart (High)

*   Smoke: Add Item to Cart, View Cart Summary
*   Regression: Update Quantity in Cart, Remove Item from Cart, Add Out-of-Stock Item (Verify Error), Cart Persistence (Refresh Page)

### Checkout & Payments (Critical)

*   Smoke: Complete Purchase (Guest / Standard)
*   Regression: Checkout with formatted Address, Apply Valid/Invalid Coupon Code, Payment Decline Simulation, Calculate Tax/Shipping correctly
