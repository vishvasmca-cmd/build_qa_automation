# Test Plan: core_automation_exercise

## Overview

This test plan outlines the testing strategy for the core_automation_exercise project, an e-commerce platform. The plan includes smoke and regression test suites, focusing on critical functionalities such as product browsing, shopping cart management, and checkout processes.

## Scope

The testing will cover the following modules:

*   Authentication (Login/Registration)
*   Product Catalog (Browsing, Search)
*   Shopping Cart (Add/Remove/Update Items)
*   Checkout & Payments

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionalities of the application. These tests are designed to be executed quickly and efficiently to ensure the system is stable and ready for further testing.

#### Smoke Suite Strategy

The following checklist was applied when designing the Smoke Suite:

1.  **Critical Paths:** Tests cover the most common and essential user flows.
2.  **Core Business Logic:** Focus on testing the primary revenue-generating or operationally critical features.
3.  **Positive Testing:** Primarily focuses on happy path scenarios with valid inputs.
4.  **No Negative Testing:** Excludes tests with invalid inputs or error conditions (unless security-critical).
5.  **Minimal Edge Cases:** Avoids complex or unusual scenarios.
6.  **Independent Tests:** Each test should be independent and not rely on the state of previous tests.
7.  **Fast Execution:** Tests should be designed for quick execution to provide rapid feedback.
8.  **High Priority:** Any failures in the smoke suite should be treated as critical and addressed immediately.

#### Smoke Test Cases

*   Navigate to Products page
*   Search for a product ('Dress')
*   Add a product to the cart
*   View the cart
*   Proceed to checkout

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, boundary analysis, and cross-module interactions.

#### Regression Test Cases

*   Login with invalid credentials
*   Search for a non-existent product
*   Update quantity in cart
*   Remove item from cart
*   Apply invalid coupon code
*   Checkout with invalid address format

## Test Environment

The tests will be executed on the following environment:

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   URL: https://automationexercise.com/

## Test Data

Test data will be used to cover various scenarios, including valid and invalid inputs.

## Entry Criteria

*   The application build is deployed to the test environment.
*   All necessary test data is prepared.

## Exit Criteria

*   All test cases in the smoke suite have passed.
*   A defined percentage of test cases in the regression suite have passed (e.g., 95%).
*   All critical and high severity defects have been resolved.
