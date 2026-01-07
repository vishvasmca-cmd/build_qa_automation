# Test Plan: core_automation_exercise

## Overview

This test plan outlines the testing strategy for the core_automation_exercise project, an e-commerce platform. The plan includes smoke and regression test suites to ensure the quality and stability of the application.

## Test Suites

### Smoke Suite

The smoke suite focuses on verifying the core functionality of the application. These tests are designed to be executed quickly and should identify any major issues that would prevent further testing.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the scope of the smoke suite:

1.  **Critical Paths:** Tests cover essential user flows like product search and adding to cart.
2.  **Core Business Logic:** Focuses on the primary function of an e-commerce site: finding and adding products.
3.  **Positive Testing:** Only valid inputs and actions are used.
4.  **No Edge Cases:** Complex scenarios and boundary conditions are excluded.
5.  **Minimal Data Variation:** A single set of data is used for each test.
6.  **Independent Tests:** Each test can be run independently without dependencies.
7.  **Fast Execution:** Tests are designed to run quickly.
8.  **High Priority:** Any failure in the smoke suite indicates a critical issue.

### Regression Suite

The regression suite provides comprehensive test coverage to ensure that new changes do not introduce defects into existing functionality. This suite includes a wider range of scenarios, including edge cases and negative testing.

## Test Modules

### Product Catalog

*   **Smoke:**
    *   Verify user can search for a product
    *   Verify user can add a product to the cart
*   **Regression:**
    *   Verify user can filter products by price
    *   Verify user can sort products by name
    *   Verify user sees appropriate message when searching for a non-existent product

### Shopping Cart

*   **Smoke:**
    *   Verify user can add item to cart
*   **Regression:**
    *   Verify user can update quantity in cart
    *   Verify user can remove item from cart
    *   Verify error message when adding out-of-stock item

