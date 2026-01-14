# Test Plan: Dyson E2E CI

## Introduction

This document outlines the test plan for the Dyson E2E CI project, focusing on end-to-end testing of critical user flows on the Dyson India website. The plan includes both smoke and regression test suites to ensure the quality and stability of the application.

## Test Scope

The tests will cover the following areas:

*   Homepage
*   Product Search
*   Product Detail Page (PDP)
*   Shopping Cart
*   Checkout Process

## Test Suites

### Smoke Suite

The smoke suite will focus on verifying the core functionality of the application. These tests are designed to be executed quickly and should identify any major issues that would prevent further testing.

#### Smoke Suite Strategy

The following 8-point checklist has been applied to define the Smoke Suite for this project:

1.  **Critical Paths:** Tests cover essential user journeys like searching for a product and adding it to the cart.
2.  **Core Business Logic:** Focuses on testing the primary flow of adding a product to the cart and navigating to checkout.
3.  **Positive Testing:** Only positive scenarios are considered (e.g., successful product search, adding to cart).
4.  **No Negative Testing:** Negative scenarios like invalid search queries are excluded.
5.  **No Complex Edge Cases:** Complex scenarios like applying discounts or using gift cards are not included.
6.  **Speed of Execution:** Tests are designed to be fast and efficient.
7.  **Independence:** Tests are independent and can be run in any order.
8.  **Environment Stability:** Assumes a stable test environment.

### Regression Suite

The regression suite will provide a more comprehensive test coverage, including alternative flows, negative scenarios, and edge cases. These tests will ensure that new changes have not introduced any regressions in existing functionality.

## Test Cases (Examples)

**Smoke Suite:**

*   Verify that a user can search for a product and view the search results.
*   Verify that a user can add a product to the cart from the PDP.
*   Verify that a user can navigate to the checkout page from the cart.

**Regression Suite:**

*   Verify that a user can search for a product using different keywords.
*   Verify that the cart updates correctly when adding or removing products.
*   Verify that the checkout process handles different payment methods.
*   Verify error messages are displayed correctly for invalid input.

## Test Environment

The tests will be executed on the following environment:

*   Browser: Chrome (latest version)
*   Operating System: Windows 10
*   URL: [https://www.dyson.in/](https://www.dyson.in/)

## Test Execution

The tests will be executed using a CI/CD pipeline. The smoke suite will be executed on every commit, while the regression suite will be executed on a nightly basis.

## Test Reporting

Test results will be reported using a test management tool. The reports will include the number of tests executed, the number of tests passed, and the number of tests failed.
