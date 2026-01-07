# Test Plan: core_automation_exercise

## Overview

This test plan outlines the testing strategy for the core_automation_exercise project, an e-commerce platform. The plan includes smoke and regression test suites, focusing on critical functionalities such as product browsing, shopping cart management, and checkout processes.

## Test Suites

### 1. Smoke Suite

The smoke suite verifies the core functionalities of the application. It is designed to be executed quickly to ensure the system's stability after deployment or code changes. If any of the smoke tests fail, the build should be rejected.

#### Smoke Suite Strategy

The following 8-point checklist was applied when designing the smoke suite:

1.  **Critical Paths:** Tests cover the most critical user flows (e.g., login, checkout).
2.  **Core Business Logic:** Focuses on testing the primary revenue-generating or operationally essential flows.
3.  **Positive Testing:** Primarily uses valid inputs and happy-path scenarios.
4.  **No Negative Testing:** Excludes tests with invalid inputs or error conditions (unless critical security).
5.  **No Complex Edge Cases:** Avoids intricate scenarios or boundary conditions.
6.  **Fast Execution:** Designed for quick execution to provide rapid feedback.
7.  **Independent Tests:** Each test should be independent and not rely on the state of others.
8.  **Limited Scope:** Covers a minimal set of functionalities to ensure basic system health.

#### Smoke Test Cases

*   **TC_SMOKE_001: Product Search and Checkout**
    *   Objective: Verify that a user can successfully search for a product, add it to the cart, and proceed to the checkout page.
    *   Steps:
        1.  Navigate to the Products page.
        2.  Search for a product (e.g., "Dress").
        3.  Add the first displayed product to the cart.
        4.  Proceed to checkout from the cart page.

### 2. Regression Suite

The regression suite is a comprehensive set of tests designed to ensure that new changes have not introduced defects into existing functionality. It covers a wide range of scenarios, including alternative flows, negative tests, and boundary conditions.

#### Regression Test Cases

*   **TC_REG_001: Product Search - No Results**
    *   Objective: Verify that the system handles searches with no results gracefully.
    *   Steps:
        1.  Navigate to the Products page.
        2.  Search for a non-existent product.
        3.  Verify that a "no results found" message is displayed.
*   **TC_REG_002: Add to Cart - Multiple Items**
    *   Objective: Verify that multiple items can be added to the cart.
    *   Steps:
        1.  Navigate to the Products page.
        2.  Add multiple products to the cart.
        3.  Verify that all added products are displayed in the cart.
*   **TC_REG_003: Checkout with different address formats**
    *   Objective: Verify that the checkout process works correctly with different address formats.
    *   Steps:
        1.  Add a product to the cart.
        2.  Proceed to checkout.
        3.  Enter an address with special characters.
        4.  Verify that the order can be placed successfully.

## Test Environment

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   URL: https://automationexercise.com/

