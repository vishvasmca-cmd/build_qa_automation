# Test Plan: core_saucedemo

## Introduction

This test plan outlines the testing strategy for the core_saucedemo e-commerce application. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Scope

The testing will cover the following modules:

*   Authentication
*   Product Catalog
*   Shopping Cart
*   Checkout & Payments

## Test Suites

### Smoke Suite

The smoke suite will focus on the critical paths and core functionalities of the application. The goal is to quickly verify that the system is in a working state.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the smoke suite for this project:

1.  **Critical Paths:** Tests cover essential user flows like login and adding to cart.
2.  **Core Business Logic:** Focuses on primary revenue/operation flows.
3.  **No Negative Testing:** Excludes negative scenarios unless critical for security.
4.  **No Complex Edge Cases:** Avoids intricate or unusual scenarios.
5.  **Minimal Test Set:** Keeps the number of tests small for quick execution.
6.  **Independent Tests:** Each test should be independent and not rely on others.
7.  **Fast Execution:** Tests should be designed for rapid completion.
8.  **High Priority:** Failures in smoke tests indicate critical issues.

#### Smoke Test Cases

*   Verify user login with valid credentials.
*   Verify product sorting by price.
*   Verify adding a product to the cart.

### Regression Suite

The regression suite will provide comprehensive coverage of the application, including alternative flows, negative scenarios, and boundary conditions. The goal is to ensure that new changes have not introduced any regressions.

#### Regression Test Cases

*   Authentication:
    *   Login with invalid password.
    *   Password reset flow.
    *   Registration with existing email.
*   Product Catalog:
    *   Filter products by category.
    *   Search for a non-existent product.
*   Shopping Cart:
    *   Update quantity in cart.
    *   Remove item from cart.
    *   Add out-of-stock item (verify error).
*   Checkout & Payments:
    *   Checkout with formatted address.
    *   Apply valid/invalid coupon code.
    *   Payment decline simulation.

## Test Environment

The tests will be executed in a stable test environment that closely resembles the production environment.

## Test Data

Realistic and representative test data will be used to ensure the validity of the tests.
